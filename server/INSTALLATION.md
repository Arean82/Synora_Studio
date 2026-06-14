# Server Installation Guide
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![OS Compatibility](https://img.shields.io/badge/os-Windows%20%7C%20Linux-green)
![Role](https://img.shields.io/badge/Role-Backend%20Core-red)

This guide will walk you through setting up the **Synora API Server** from scratch. 
Because Synora Studio is modular, the server is the **first component you must install and run**, as all other parts of the platform connect to it.

---

## 💻 1. Developer Deployment (Source Code)

This is the standard approach for active development and local testing.

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

### Step 4: Start the Server
```bash
cd server
python server.py
```
*(Note: You will hit the `CLI AUTHENTICATION GATE` on first boot. See the section below for details).*

---

## 🚀 2. Production Deployment (Systemd Background Service)

For production deployments on a Linux VPS, you should run the server as a persistent background daemon.

1. Create a service file:
```bash
sudo nano /etc/systemd/system/synora-server.service
```

2. Add the following configuration (replace `/path/to/Synora_Studio` with your actual path):
```ini
[Unit]
Description=Synora Studio API Server
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/Synora_Studio
ExecStart=/path/to/Synora_Studio/venv/bin/python server/server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-server
sudo systemctl start synora-server
```

---

## 🛡️ 3. Production Deployment (NGINX Reverse Proxy)

If you are exposing the API Server to the internet, you should place it behind an NGINX reverse proxy with SSL.

1. Install NGINX: `sudo apt install nginx`
2. Create a config: `sudo nano /etc/nginx/sites-available/synora-server`
3. Add the configuration:
```nginx
server {
    listen 80;
    server_name api.synorastudio.in;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```
4. Enable the site and restart NGINX:
```bash
sudo ln -s /etc/nginx/sites-available/synora-server /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Step 5: Inject SSL via Certbot (Production Requirement)
Since the API server manages sensitive payloads, you **must** encrypt the traffic using SSL in production.
Install Certbot and run it against NGINX. Certbot will automatically read the `server_name` block above, provision a Let's Encrypt SSL Certificate, and automatically inject the port `443` secure routing configuration into the file.
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.synorastudio.in
```

---

## 📦 4. Production Compilation (PyInstaller)

If you wish to distribute the API Server to client hardware without requiring Python to be installed, compile it into a standalone binary.

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Compile the Binary:
```bash
pyinstaller --noconfirm --onedir --name "Synora_Server" server/server.py
```
*(Note: We do NOT use `--windowed` for the server because we need the terminal stdout for logs).*

3. Run the compiled binary:
```bash
./dist/Synora_Server/Synora_Server
```

---

## 🛑 5. What Happens Next? (The CLI Authentication Gate)

The very first time you start the server, you will see a prompt that looks like this:

```
[INFO] Starting isolated backend server...
==================================================
 LLM CHAT APP: CLI AUTHENTICATION GATE
==================================================
No active session found. Please configure your provider.
```

### How to proceed:
1. **Select your Platform:** Type the number corresponding to your preferred AI provider (e.g., type `1` for OpenAI) and press **Enter**.
2. **Select the Model:** Type the number for the model you want and press **Enter**.
3. **Enter your API Key:** Paste your secret API key. *Note: When you paste the password, nothing will show up on the screen for security reasons. Just press **Enter**.*
4. **Success!** The server will securely encrypt this key in your local storage. You only have to do this once!

### How to Bypass this Prompt entirely:
If you are just doing local development, you can force the server to boot unauthenticated by setting an environment variable:
- **Linux:** `ALLOW_UNAUTHENTICATED_SERVER="1" python server/server.py`
- **Windows:** `$env:ALLOW_UNAUTHENTICATED_SERVER="1"; python server\server.py`
