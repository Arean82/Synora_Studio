# Headless CLI Client Installation Guide

This guide will walk you through setting up the **Synora Headless CLI Client**. 
This module provides a lightweight, text-based interface for interacting with the backend. 

Because Synora is strictly decoupled, **you must ensure the API Server is already running on port 5000** before the CLI can send requests to it.

---

## 🐧 Linux / Ubuntu & 🪟 Windows Setup

Since this is a lightweight terminal client, the setup process is identical across operating systems.

**Step 1: Open Terminal or PowerShell**
Navigate to the root directory of the repository.

**Step 2: Activate your Virtual Environment**
Ensure you activate the main environment you created for the server:
- **Linux:** `source venv/bin/activate`
- **Windows:** `.\venv\Scripts\activate`

**Step 3: Run the CLI Client**
Navigate to the headless directory and launch the client:
```bash
cd headless
python run_cli.py
```

---

## 🛑 The Authentication Gate

When you run `run_cli.py` for the first time, you will encounter the **CLI Authentication Gate**. 

This allows you to securely inject your AI Provider API Keys (like OpenAI or Google Gemini) into the local OS keychain without needing the Desktop GUI.

1. **Select Platform:** Choose your preferred SDK from the numbered list.
2. **Enter API Key:** Paste your secret token when prompted.
3. **Success:** The CLI will save the key to your system's secure vault and establish a connection to the running API Server on port 5000.
