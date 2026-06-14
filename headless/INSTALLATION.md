# Headless CLI Client Installation Guide
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![OS Compatibility](https://img.shields.io/badge/os-Windows%20%7C%20Linux-green)
![Framework](https://img.shields.io/badge/Interface-Terminal-black)

This guide will walk you through setting up the **Synora Headless CLI Client**. 
This is a lightweight, terminal-based interaction suite designed for pure speed and server administration without Graphical UI overhead.

Because Synora is modular, the headless app **requires the API Server to be running** first. Please ensure you have completed `synora_server/INSTALLATION.md` before proceeding.

---

## 💻 1. Developer Deployment (Source Code)

This is the standard approach for active development, script automation, and daily use.

### Step 1: Clone the Repository
Open your Terminal or PowerShell and clone the codebase to a generic directory like `~/Downloads` or `~/projects`.
```bash
cd ~/Downloads
git clone https://github.com/Synora/Synora_Studio.git
cd Synora_Studio
```

### Step 2: Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Navigate to the headless directory and run the main entry point:
```bash
cd headless
python headless.py --cli
```

---

## 🚀 2. Production Deployment (Systemd Integration)

Typically, the Headless client is run interactively on-demand by users (`python headless.py --cli`). However, if you are wrapping the headless client into an automated pipeline or persistent shell loop, you can run it via Systemd.

1. Create a service file:
```bash
sudo nano /etc/systemd/system/synora-headless-bot.service
```

2. Add the following configuration (replace `/path/to/Synora_Studio` with your actual path):
```ini
[Unit]
Description=Synora Studio Headless Bot
After=network.target synora-server.service

[Service]
User=your_username
WorkingDirectory=/path/to/Synora_Studio
# Run an automated script utilizing the headless pipeline
ExecStart=/path/to/Synora_Studio/venv/bin/python headless/headless.py --execute-automation-script
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-headless-bot
sudo systemctl start synora-headless-bot
```

---

## 📦 3. Production Compilation (PyInstaller)

If you wish to distribute the lightweight CLI client to users without requiring Python installations, you can freeze it into a single binary.

### Step 1: Install PyInstaller
Ensure your virtual environment is activated, then install the compiler:
```bash
pip install pyinstaller
```

### Step 2: Compile the Binary
Run the following command from the root directory.
```bash
pyinstaller --noconfirm --onedir --name "Synora_CLI" headless/headless.py
```

### Step 3: Distribute
Once the build completes, the standalone compiled application will be located in the `dist/Synora_CLI/` directory. You can distribute this lightweight folder to end users.
They can run it directly:
```bash
./dist/Synora_CLI/Synora_CLI --cli
```
