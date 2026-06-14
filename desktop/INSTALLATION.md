# Desktop Client Installation Guide
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![OS Compatibility](https://img.shields.io/badge/os-Windows%20%7C%20Linux-green)
![Framework](https://img.shields.io/badge/GUI-PySide6-red)

This guide will walk you through setting up the **Synora Studio Desktop Client**. The Desktop application provides a native, highly responsive Graphical User Interface (GUI) to interact with your AI agents. 

Because Synora is modular, the desktop app **requires the API Server to be running** first. Please ensure you have completed `synora_server/INSTALLATION.md` before proceeding.

---

## 💻 1. Developer Deployment (Source Code)

This is the standard approach for active development, local testing, and daily use.

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
*Linux Note: You may require system-level GUI dependencies for PyQt6: `sudo apt install libgl1-mesa-glx libegl1-mesa`*
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Navigate to the desktop directory and run the main entry point:
```bash
cd desktop
python desktop.py
```

---

## 🚀 2. Production Deployment (Systemd Background Service)

If you are running a Linux desktop environment (like GNOME or KDE) and want the Desktop client to launch automatically in the background as a daemon:

1. Create a service file:
```bash
sudo nano /etc/systemd/system/synora-desktop.service
```

2. Add the following configuration (replace `/path/to/Synora_Studio` with your actual path, e.g., `/home/user/Downloads/Synora_Studio`):
```ini
[Unit]
Description=Synora Studio Desktop Client
After=network.target synora-server.service

[Service]
User=your_username
WorkingDirectory=/path/to/Synora_Studio
Environment=DISPLAY=:0
ExecStart=/path/to/Synora_Studio/venv/bin/python desktop/desktop.py
Restart=always

[Install]
WantedBy=graphical.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-desktop
sudo systemctl start synora-desktop
```

---

## 🌐 3. X11 Cloud Deployment (Remote GUI)

If you install the Desktop App directly on a headless Linux Ubuntu server, you can natively run the app on the server while projecting the Graphical User Interface (GUI) directly to your local Windows machine using **X11 Forwarding**.

### Prerequisites
1. Ensure your Ubuntu server has the GUI dependencies installed (see `README.md`).
2. Install an X-Server on your local Windows machine (e.g., [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/)).

### Connection Steps
1. Open your SSH client (PuTTY, MobaXterm, or WSL).
2. Connect to your server with X11 forwarding enabled:
   ```bash
   ssh -X admin@your-server-ip
   # or
   ssh -Y admin@your-server-ip
   ```
3. Activate the virtual environment and run the Desktop App:
   ```bash
   cd /path/to/Synora_Studio
   source venv/bin/activate
   python desktop/desktop.py
   ```
The PySide6 window will open natively on your local Windows desktop, but it will be executing natively on the cloud server.

> [!TIP]
> **Graceful Headless Degradation**: If you execute `desktop.py` over SSH without `ssh -X` (or your server lacks `libxcb`), the Desktop App will gracefully catch the X11 connection failure. Instead of crashing, it will output clear troubleshooting instructions and instantly route you into the interactive Headless Engine mode, allowing the platform to still start in the background!

---

## 📦 4. Production Compilation (PyInstaller)

If you wish to distribute the application to end-users without requiring them to install Python or manage virtual environments, you can freeze the code into a standalone executable using `PyInstaller`.

### Step 1: Install PyInstaller
Ensure your virtual environment is activated, then install the compiler:
```bash
pip install pyinstaller
```

### Step 2: Compile the Binary
Run the following command from the root directory. The `--windowed` flag ensures no terminal window opens behind the GUI.
```bash
pyinstaller --noconfirm --onedir --windowed --name "Synora_Desktop" --add-data "desktop/ui_assets;ui_assets" desktop/desktop.py
```

### Step 3: Distribute
Once the build completes, the standalone compiled application will be located in the `dist/Synora_Desktop/` directory. You can zip this folder and distribute it to production endpoints.
