# AI-Powered Security Code Reviewer & Git Hook

## 📝 Overview

This project is a proof-of-concept demonstrating how local, privacy-focused Large Language Models (LLMs) can be integrated into a developer's workflow to perform real-time security analysis on Python code.

The tool has two main components:
1.  An **interactive web application** for on-demand code scanning.
2.  An automated **Git pre-commit hook** that prevents insecure code from being committed to the repository.

The entire analysis is performed locally using **Ollama**, ensuring that your source code never leaves your machine.

## ✨ Features

* **Interactive Web UI:** A simple Streamlit interface to paste and analyze code snippets.
* **Automated Git Hook:** Automatically scans staged Python files during a `git commit` and blocks the commit if vulnerabilities are detected.
* **Powered by Local LLMs:** Uses models like `qwen:4b` or `codellama:7b` running via Ollama.
* **Privacy-Focused:** Your code is never sent to a third-party API.
* **Structured & Reliable:** The git hook uses a structured JSON format for reliable, programmatic analysis of the AI's response.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
* [Python 3.8+](https://www.python.org/downloads/)
* `pip` (Python's package installer)
* [Git](https://git-scm.com/downloads)
* [Ollama](https://ollama.com/) (Make sure the desktop application is running)

## ⚙️ Setup Instructions

Follow these steps to get the project up and running.

### 1. Clone the Repository
First, clone this project to your local machine.
```bash
git clone <your-repository-url>
cd <your-repository-name>