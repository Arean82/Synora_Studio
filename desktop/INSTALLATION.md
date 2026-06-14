# Desktop Client Installation Guide (Beginner Friendly)

This guide will walk you through setting up the **Synora Studio Desktop Client**. 
The Desktop application provides a native, highly responsive Graphical User Interface (GUI) to interact with your AI agents. 

Because Synora is modular, the desktop app **requires the API Server to be running on port 5000** first. Please ensure you have completed `server/INSTALLATION.md` before proceeding.

Choose your operating system below and follow the exact commands in your terminal.

---

## 🪟 Windows (Development & Daily Use)

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

**Step 4: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Start the Desktop App**
Navigate to the desktop directory and run the main entry point:
```powershell
cd desktop
python main.py
```

---

## 🐧 Linux / Ubuntu

**Step 1: Open Terminal**
Navigate to the root directory of the repository.

**Step 2: Create a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
```

**Step 3: Activate the Virtual Environment**
```bash
source venv/bin/activate
```

**Step 4: Install Dependencies**
Linux may require system-level GUI dependencies for PyQt6 to render correctly.
```bash
sudo apt update
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
pip install -r requirements.txt
```

**Step 5: Start the Desktop App**
```bash
cd desktop
python main.py
```

---

## 🔒 Security Vault Initialization

The very first time you launch the desktop app, it will attempt to sync with your Operating System's secure keychain (e.g., Windows Credential Manager or Linux Secret Service). 

If you already provided your API keys to the backend server via the CLI Authentication Gate, the Desktop App will automatically detect them and log you in immediately.

If you ever need to change your API keys, you can click the `Settings (Gear Icon) -> Security Vault` inside the desktop app.
