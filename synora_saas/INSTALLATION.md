# Web Portal Installation Guide
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![OS Compatibility](https://img.shields.io/badge/os-Windows%20%7C%20Linux-green)
![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20Socket.IO-red)

This guide will walk you through setting up the **Synora SaaS Web Portal**. 
Because Synora Studio is modular, the web portal operates completely independently but **it requires the API Server to be running** to function. Ensure you have completed the `synora_server/INSTALLATION.md` steps first.

---

## 💻 1. Developer Deployment (Source Code)

This is the standard approach for active development, frontend customization, and local testing.

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

### Step 4: Start the Web Portal
```bash
cd web
python saas.py
```
*Navigate to `http://localhost:8888` in your browser.*

---

## 🚀 2. Production Deployment (Systemd Background Service)

For production SaaS deployments, run the portal as a persistent daemon.

1. Create a service file:
```bash
sudo nano /etc/systemd/system/synora-web.service
```

2. Add the following configuration (replace `/path/to/Synora_Studio` with your actual path):
```ini
[Unit]
Description=Synora Studio Web Portal
After=network.target synora-server.service

[Service]
User=your_username
WorkingDirectory=/path/to/Synora_Studio
ExecStart=/path/to/Synora_Studio/venv/bin/python synora_synora_saas/synora_saas.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-web
sudo systemctl start synora-web
```

---

## 🛡️ 3. Production Deployment (NGINX Reverse Proxy)

If you are exposing the Web Portal to end-users on the internet, put it behind NGINX.

1. Install NGINX: `sudo apt install nginx`
2. Create a config: `sudo nano /etc/nginx/sites-available/synora-web`
3. Add the configuration:
```nginx
server {
    listen 80;
    server_name synorastudio.in www.synorastudio.in;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```
4. Enable the site and restart NGINX:
```bash
sudo ln -s /etc/nginx/sites-available/synora-web /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Step 5: Inject SSL via Certbot (Production Requirement)
To secure the SaaS dashboard from man-in-the-middle attacks, you **must** encrypt the traffic using SSL in production.
Install Certbot and run it against NGINX. Certbot will automatically read the `server_name` block above, provision a Let's Encrypt SSL Certificate, and automatically inject the port `443` secure routing configuration into the file.
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d synorastudio.in -d www.synorastudio.in
```

---

## 📦 4. Production Compilation (PyInstaller)

If you wish to distribute the Web Portal to local on-premise hardware without setting up Python, compile it into a standalone binary.

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Compile the Binary:
```bash
pyinstaller --noconfirm --onedir --name "Synora_Web" --add-data "synora_saas/templates;templates" --add-data "synora_saas/static;static" synora_synora_saas/synora_saas.py
```
*(Note: We do NOT use `--windowed` because web servers require standard output for request logging).*

3. Run the compiled binary:
```bash
./dist/Synora_Web/Synora_Web
```

---

## 🌐 5. First Time Setup

Once the web server is running:
1. Navigate to the web portal URL.
2. Since there are no user accounts yet, you will be prompted to create the first Tenant/Admin account.
3. The web portal will securely hash your password and store it in the Tenant Database.
4. Once logged in, the Web Portal will connect to the API Server running in the background to handle all LLM and RAG capabilities.
