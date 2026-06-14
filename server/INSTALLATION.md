# Server Installation Guide (Beginner Friendly)

This guide will walk you through setting up the **Synora API Server** from scratch. 
Because Synora Studio is modular, the server is the **first component you must install and run**, as all other parts of the platform connect to it.

Choose your operating system below and follow the exact commands in your terminal.

---

## 🐧 Linux / Ubuntu (Production & Dev)

**Step 1: Open Terminal**
Navigate to the root directory of the repository (where the main `requirements.txt` file is located).

**Step 2: Create a Virtual Environment (Recommended)**
It is best practice to keep Python packages isolated.
```bash
python3 -m venv venv
```

**Step 3: Activate the Virtual Environment**
```bash
source venv/bin/activate
```
*(You should see `(venv)` appear at the beginning of your command line prompt).*

**Step 4: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Start the Server**
Navigate into the `server` directory and run the engine:
```bash
cd server
python run_server.py
```

---

## 🪟 Windows (Development)

**Step 1: Open PowerShell**
Navigate to the root directory of the repository.

**Step 2: Create a Virtual Environment**
```powershell
python -m venv venv
```

**Step 3: Activate the Virtual Environment**
```powershell
.\venv\Scripts\activate
```
*(You should see `(venv)` appear at the beginning of your PowerShell prompt).*

**Step 4: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Start the Server**
```powershell
python server\run_server.py
```

---

## 🛑 What Happens Next? (The CLI Authentication Gate)

The very first time you start the server, you will see a prompt that looks like this:

```
[INFO] Starting isolated backend server...
==================================================
 LLM CHAT APP: CLI AUTHENTICATION GATE
==================================================
No active session found. Please configure your provider.

Step 1: Select Platform/SDK Group:

Select Platform (1-x) [1]:
```

### What is this?
Because the server requires an AI brain to function (like OpenAI, Google Gemini, or local models), it pauses the boot process to ask you for your API credentials.

### How to proceed (Step-by-Step):

1. **Select your Platform:** Type the number corresponding to your preferred AI provider (e.g., type `1` for OpenAI) and press **Enter**.
2. **Select the Model:** The terminal will list available models for that provider (e.g., `gpt-4`). Type the number for the model you want and press **Enter**.
3. **Enter your API Key:** The prompt will say `Enter your Provider API Key:`. 
   - Paste your secret API key (e.g., your OpenAI `sk-...` key). 
   - *Note: When you paste or type the password, nothing will show up on the screen for security reasons. Just press **Enter**.*
4. **Success!** The server will securely encrypt this key in your local storage, connect to the AI, and finish booting. You will see:
   `[INFO] Starting Socket.IO REST Multiplexer on port 5000...`

You only have to do this once! The server will remember your choice for the next time.

### How to Bypass this Prompt entirely:
If you are just doing local development and don't want to enter an API key yet, you can force the server to boot unauthenticated by setting an environment variable before running the script:

**Linux / Ubuntu:**
```bash
ALLOW_UNAUTHENTICATED_SERVER="1" python server/run_server.py
```

**Windows (PowerShell):**
```powershell
$env:ALLOW_UNAUTHENTICATED_SERVER="1"; python server\run_server.py
```
