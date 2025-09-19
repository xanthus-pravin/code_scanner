import streamlit as st
from reviewer import analyze_code # Import our AI function

# Example of vulnerable code for the user to try
VULNERABLE_CODE_EXAMPLE = """
import os
import subprocess

def check_website_status(url):
    # Vulnerability: Command Injection
    command = "ping -c 1 " + url 
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
"""

# Page configuration
st.set_page_config(page_title="AI Security Code Reviewer", layout="wide")

# Title and description
st.title("🤖 AI Security Code Reviewer")
st.write("Paste a Python code snippet below and let a local AI model (Code Llama) analyze it for security vulnerabilities.")

# Text area for code input
st.subheader("Enter Code Snippet")
code_input = st.text_area("Analyze your Python code:", height=300, value=VULNERABLE_CODE_EXAMPLE)

# Analyze button
if st.button("Analyze Code ✨"):
    if code_input:
        with st.spinner("The AI is thinking... This may take a moment."):
            analysis_result = analyze_code(code_input)
            st.subheader("Analysis Result")
            st.markdown(analysis_result)
    else:
        st.warning("Please enter some code to analyze.")