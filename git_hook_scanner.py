import sys
import argparse
from reviewer import analyze_code # Reuse our existing Ollama logic

# Keywords to look for in the AI's response to decide if the commit should fail
VULNERABILITY_KEYWORDS = ["vulnerability", "insecure", "risk", "exploit", "injection", "hardcoded"]

def scan_files(file_paths):
    """Scans a list of files and returns True if any are insecure."""
    insecure_files_found = 0
    
    for file_path in file_paths:
        print(f"\n--- Scanning {file_path} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If the file is empty, skip it
            if not content.strip():
                continue

            analysis_result = analyze_code(content).lower()
            
            # Check if any of our keywords are in the AI's response
            if any(keyword in analysis_result for keyword in VULNERABILITY_KEYWORDS):
                print(f"\n🚨 INSECURE CODE DETECTED IN {file_path} 🚨")
                print("--- AI Analysis ---")
                print(analysis_result)
                print("---------------------")
                insecure_files_found += 1
            else:
                print(f"✅ Code appears secure.")

        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
    
    return insecure_files_found > 0

if __name__ == "__main__":
    # The pre-commit framework passes the staged files as arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    if scan_files(args.files):
        print("\nCOMMIT REJECTED: Insecure code found. Please fix the issues above before committing.")
        sys.exit(1) # Exit with a non-zero status to block the commit
    else:
        print("\nCOMMIT ACCEPTED: All scanned files passed the security check.")
        sys.exit(0) # Exit with zero to allow the commit