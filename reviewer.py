import requests
import json

OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"

def _extract_json_from_string(s):
    """
    Extracts a JSON object from a string, even if it's embedded in other text
    or a markdown code block.
    """
    # Find the first '{' and the last '}' to get the JSON substring
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        json_str = s[start:end+1]
        return json.loads(json_str) # This can still raise JSONDecodeError
    raise json.JSONDecodeError("No valid JSON object found in the string.", s, 0)

def analyze_code(code_snippet, response_type='text'):
    """
    Sends a code snippet to a local LLM for security analysis.
    - response_type 'text': Returns a natural language string.
    - response_type 'json': Returns a Python dictionary based on a structured prompt.
    """
    
    if response_type == 'json':
        system_prompt = """
        You are a security code scanner. Analyze the user's code for security vulnerabilities.
        Respond ONLY with a single JSON object of the format {"isSecure": boolean, "reason": "A brief explanation."}.
        """
    else:
        system_prompt = """
        You are an expert cybersecurity code reviewer. Your task is to analyze the following code snippet for any security vulnerabilities.
        List any vulnerabilities you find, explain the potential risk of each one, and suggest a secure way to fix it.
        If you find no vulnerabilities, please state that the code appears to be secure.
        """

    user_prompt = f"Please review this code:\n```python\n{code_snippet}\n```"
    
    try:
        payload = {
            "model": "qwen3:4b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        
        if response_type == 'json':
            payload['format'] = 'json'

        # --- START DEBUG BLOCK (LOGS TO FILE) ---
        # This will create a file in your project folder with the request body.
        try:
            json_string_to_send = json.dumps(payload, indent=2)
            with open("debug_log.txt", "w", encoding="utf-8") as f:
                f.write("PAYLOAD SENT TO OLLAMA:\n\n")
                f.write(json_string_to_send)
        except Exception as e:
            with open("debug_log.txt", "w") as f:
                f.write(f"Error creating debug log: {e}")
        # --- END DEBUG BLOCK ---

        print(f"--- Sending prompt to Ollama (model: qwen:4b, mode: {response_type})... ---")
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=12000)
        response.raise_for_status()
        response_json = response.json()
        
        raw_content = response_json.get("message", {}).get("content", "")
        
        if response_type == 'json':
            # Use the robust extraction function
            return _extract_json_from_string(raw_content)
        else:
            return raw_content

    except requests.exceptions.RequestException as e:
        # FAIL-CLOSED: If we can't connect to the AI, assume the code is insecure to be safe.
        error_reason = f"Error connecting to Ollama: {e}"
        print(f"DEBUG: RequestException occurred. Reason: {error_reason}") # Added for clarity
        return {"isSecure": False, "reason": error_reason} if response_type == 'json' else error_reason
    except json.JSONDecodeError:
        # FAIL-CLOSED: If the AI gives a malformed response, we can't trust it.
        error_reason = "Error: Failed to parse JSON from Ollama's response."
        print(f"DEBUG: JSONDecodeError occurred. Raw content was: {raw_content}") # Added for clarity
        return {"isSecure": False, "reason": error_reason} if response_type == 'json' else error_reason