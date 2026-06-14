# Companion App Toolkit Installation Guide
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![OS Compatibility](https://img.shields.io/badge/os-Windows%20%7C%20Linux-green)
![Privilege](https://img.shields.io/badge/Privilege-Administrator-red)

The **Companion App Toolkit** is a highly restricted, privileged administrative tool used by DevOps engineers and System Administrators to manage the Synora ecosystem. 

Because it hooks into the core database and active backend services, **you must ensure the API Server is already configured and running** before using the toolkit.

---

## 💻 1. Developer Deployment (Source Code)

This is the standard approach for active development, local database migrations, and daily maintenance.

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

### Step 4: Run the Toolkit
Navigate to the companion module and start the interactive GUI or CLI:
```bash
cd companion_app
python companion_app.py
```

---

## 🚀 2. Production Deployment (Systemd Background Service)

Typically, the Companion App is an on-demand utility, meaning it does **not** run as a persistent background daemon.

However, if you are utilizing the Companion App to orchestrate automated scheduled backups via cron jobs, you can create a one-shot systemd timer or cron script:

1. Create an executable bash script `backup.sh`:
```bash
#!/bin/bash
/path/to/Synora_Studio/venv/bin/python /path/to/Synora_Studio/companion_app/companion_app.py --action backup --target-dir /var/backups/synora
```
2. Add it to `crontab -e`:
```bash
0 2 * * * /path/to/backup.sh
```

---

## 🌐 3. X11 Cloud Deployment (Remote GUI)

If you install the Companion App directly on a headless Linux Ubuntu server, you do not need to rewrite complex SSH tunneling scripts. You can natively run the app on the server while projecting the Graphical User Interface (GUI) directly to your local Windows machine using **X11 Forwarding**.

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
3. Activate the virtual environment and run the Companion App:
   ```bash
   cd /path/to/Synora_Studio
   source venv/bin/activate
   python companion_app/companion_app.py
   ```
The PySide6 window will open natively on your local Windows desktop, but it will be executing natively on the cloud server alongside the production databases!

> [!TIP]
> **Graceful Headless Degradation**: If you forget to use `ssh -X` or your server lacks `libxcb`, the Companion App will gracefully catch the X11 connection failure. Instead of crashing violently, it will print troubleshooting steps and instantly reroute you into the highly-capable Terminal CLI interface!

> [!IMPORTANT]
> **Zero-Trust Passphrase Architecture**: When utilizing the Companion App for Piggybacked Remote SSH Database Administration, you do NOT have to save your Private Key Passphrase inside the Desktop App config. If the key is encrypted and no passphrase was saved, the Companion App will dynamically detect the SSH handshake failure and prompt you to type your passphrase natively in the interactive console!
---

## 📦 4. Production Compilation (PyInstaller)

If you wish to distribute the administrative toolkit to specific IT staff without giving them the raw Python source code, you can compile it.

### Step 1: Install PyInstaller
Ensure your virtual environment is activated, then install the compiler:
```bash
pip install pyinstaller
```

### Step 2: Compile the Binary
Run the following command from the root directory.
```bash
pyinstaller --noconfirm --onedir --windowed --name "Synora_Admin" --add-data "companion_app/ui_assets;ui_assets" companion_app/companion_app.py
```

### Step 3: Distribute
Once the build completes, the standalone compiled application will be located in the `dist/Synora_Admin/` directory. You can distribute this executable to authorized DevOps personnel.

---

## 📦 Core Feature: Unified Database Migration (`--action migrate`)

The Companion App toolkit acts as the **Single Source of Truth** for all database migrations. 

If you are scaling from a local Turso/SQLite database to an Enterprise Database (PostgreSQL/MySQL), you can launch the interactive relocation wizard to securely transfer all data without zero loss:

```bash
cd companion_app
python companion_app.py --action migrate
```

## 🔑 Core Feature: Universal Admin Credentials Recovery (`--action reset-admin`)

If you completely lose access to the system, the Companion App contains a native master reset hook that will globally synchronize the Master Administrator credentials across the SaaS Tenant DB, Desktop Application, and API Server.

```bash
cd companion_app
python companion_app.py --action reset-admin --random-password
```
*(You can also use `--custom-password "my_password"` instead of `--random-password`)*
