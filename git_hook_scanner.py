import sys
import json
import subprocess
from reviewer import analyze_code

# --- CONFIGURATION ---
# Define the list of files to skip at the top of the script.
SKIP_FILES = [
    "git_hook_scanner.py",
    "reviewer.py"
]

def get_staged_files():
    """Asks Git for a list of staged Python files."""
    try:
        command = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        all_files = result.stdout.strip().split("\n")
        python_files = [f for f in all_files if f.endswith(".py") and f]
        return python_files
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def scan_files(file_paths):
    """Scans a list of files and returns True if any are insecure."""
    insecure_files_found = 0
    
    for file_path in file_paths:
        # --- NEW LOGIC: Check if the file should be skipped ---
        if file_path in SKIP_FILES:
            print(f"\n--- Skipping {file_path} (in skip list) ---")
            continue # Move to the next file in the loop

        print(f"\n--- Scanning {file_path} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if not content.strip():
                continue

            analysis_result = analyze_code(content, response_type='json')
            
            is_definitely_secure = False
            if isinstance(analysis_result, dict):
                if analysis_result.get('isSecure') is True:
                    is_definitely_secure = True
            
            if is_definitely_secure:
                print(f"✅ Code appears secure.")
            else:
                print(f"\n*** POTENTIAL INSECURITY DETECTED IN {file_path} ***")
                reason = analysis_result.get('reason', 'AI failed to provide a valid reason.') if isinstance(analysis_result, dict) else str(analysis_result)
                print(f"--- AI Analysis ---\n{reason}\n---------------------")
                insecure_files_found += 1
        except Exception as e:
            print(f"An unexpected error occurred while scanning {file_path}: {e}")
            insecure_files_found += 1
    
    return insecure_files_found > 0

if __name__ == "__main__":
    staged_files = get_staged_files()
    
    if not staged_files:
        print("No staged Python files found in this commit.")
        sys.exit(0)
    
    # The main block no longer needs to filter the list.
    # It passes all staged python files directly to the scanner.
    if scan_files(staged_files):
        print("\nCOMMIT REJECTED: Insecure code or an analysis error was detected.")
        sys.exit(1)
    else:
        print("\nCOMMIT ACCEPTED: All scanned files passed the security check.")
        sys.exit(0)