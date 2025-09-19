import requests
import json

# Corrected endpoint for chat models
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"

def analyze_code(code_snippet):
    """
    Sends a code snippet to a local LLM for security analysis using the chat endpoint.
    """
    # The system prompt sets the persona and instructions for the AI
    system_prompt = """
    You are an expert cybersecurity code reviewer. Your task is to analyze the following code snippet for any security vulnerabilities.
    List any vulnerabilities you find, explain the potential risk of each one, and suggest a secure way to fix it.
    If you find no vulnerabilities, please state that the code appears to be secure.
    """
    
    # The user prompt contains the code to be analyzed
    user_prompt = f"Please review this code:\n```python\n{code_snippet}\n```"

    try:
        # The payload for the /api/chat endpoint uses a "messages" array
        payload = {
            "model": 'tinyllama',#"codellama:7b",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            "stream": False
        }

        print("----")
        print(payload)
        print("----")
        print("--- Sending prompt to Ollama chat endpoint... ---")
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=24000)
        response.raise_for_status()

        response_json = response.json()
        
        # The response is inside a 'message' object, under the 'content' key
        return response_json.get("message", {}).get("content", "Error: Could not parse the response content.")

    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}. Please ensure Ollama is running."
    except json.JSONDecodeError:
        return "Error: Could not decode the JSON response from Ollama."