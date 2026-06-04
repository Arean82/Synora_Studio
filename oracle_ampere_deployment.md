# Oracle Cloud Enterprise Deployment & Compilation Manual

This is the complete, end-to-end production manual for deploying Synora Studio on an Oracle Cloud Ampere A1 server. 
It follows strict Linux production standards: compiling all modules, placing binaries in `/opt/synora`, managing them with `systemd`, and serving them through `Nginx`.

---

## Phase 1: Server Initialization
First, we acquire the codebase and prepare the Linux environment with required compilers and Docker for the vector database.

### 1. Download the Codebase
```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/Arean82/Synora_Studio.git
cd Synora_Studio
```

### 2. Install Native Dependencies & Nginx
```bash
sudo apt install -y python3-pip python3-venv build-essential python3-dev \
                    libsecret-1-0 dbus-x11 gnome-keyring nginx
```

### 3. Start Qdrant Vector Database
Because ARM servers cannot natively compile Qdrant, we deploy the official Docker container.
```bash
# Install Docker CE
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start the Qdrant database on port 6333
sudo docker run -d --name qdrant -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage -e QDRANT__SERVICE__ENABLE_CORS=true qdrant/qdrant
```

---

## Phase 2: Compilation Phase
We will set up the build environment and compile the 4 distinct application modules into standalone Linux executables.

### 1. Build Environment Setup
```bash
# Ensure you are in the root directory
cd /home/ubuntu/Synora_Studio

# Create and activate Python environment
python3 -m venv venv
source venv/bin/activate

# Install requirements and the PyInstaller compiler
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Compile Core Servers
```bash
# Compile Backend API Server
cd /home/ubuntu/Synora_Studio/server
pyinstaller server.spec

# Compile Web SaaS Portal
cd /home/ubuntu/Synora_Studio/web
pyinstaller web.spec
```

### 3. Compile Operator Tools
```bash
# Compile Admin Reset Tool
cd /home/ubuntu/Synora_Studio/operator_tools/admin_reset
pyinstaller reset_admin.spec

# Compile Companion Operation Tool
cd /home/ubuntu/Synora_Studio/operator_tools/companion
pyinstaller companion_operation.spec
```

---

## Phase 3: System Installation
A production server does not run executables out of a downloaded git repository. We will move the compiled binaries into the standard `/opt/` Linux directory.

### 1. Create Production Directories
```bash
sudo mkdir -p /opt/synora/bin
sudo mkdir -p /var/log/synora
sudo chown -R ubuntu:ubuntu /opt/synora
sudo chown -R ubuntu:ubuntu /var/log/synora
```

### 2. Move Compiled Binaries
Run these commands to move the 4 compiled executables to the system binary folder:
```bash
cd /home/ubuntu/Synora_Studio

# Move Core Servers
cp server/dist/server/API_Server /opt/synora/bin/
cp web/dist/web/SaaS_Web_Portal /opt/synora/bin/

# Move Operator Tools
cp operator_tools/admin_reset/dist/reset_admin/reset_admin /opt/synora/bin/
cp operator_tools/companion/dist/companion_operation/companion_operation /opt/synora/bin/

# Ensure they are executable
chmod +x /opt/synora/bin/*
```

---

## Phase 4: Service Deployment
We will create native Linux `systemd` services. This ensures the applications run silently in the background, restart automatically if they crash, and auto-start when the server reboots.

### 1. Create Backend Server Service
```bash
sudo nano /etc/systemd/system/synora-api.service
```
Paste the following:
```ini
[Unit]
Description=Synora Studio API Server
After=network.target docker.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/synora/bin
Environment="QDRANT_URL=http://localhost:6333"
ExecStart=/opt/synora/bin/API_Server
Restart=always
StandardOutput=append:/var/log/synora/api.log
StandardError=append:/var/log/synora/api_error.log

[Install]
WantedBy=multi-user.target
```

### 2. Create Web Portal Service
```bash
sudo nano /etc/systemd/system/synora-web.service
```
Paste the following:
```ini
[Unit]
Description=Synora Studio Web SaaS Portal
After=network.target synora-api.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/synora/bin
Environment="QDRANT_URL=http://localhost:6333"
ExecStart=/opt/synora/bin/SaaS_Web_Portal
Restart=always
StandardOutput=append:/var/log/synora/web.log
StandardError=append:/var/log/synora/web_error.log

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-api synora-web
sudo systemctl start synora-api synora-web
```

---

## Phase 5: Nginx SSL Reverse Proxy & Certbot
Instead of accessing the server on Port 8888, we will use Nginx and Certbot to securely route HTTPS (Port 443) web traffic to your application.

> **IMPORTANT PRE-REQUISITE:** Before continuing, you MUST purchase a domain name (e.g., `yourwebsite.com`) and point its DNS "A Record" to your Oracle Server's Public IP address. Certbot cannot generate SSL certificates for bare IP addresses.

### Option A: Standard Deployment (Port 80 + 443)
*Recommended: This leaves Port 80 open so Certbot can auto-renew your SSL certificate every 90 days, while Nginx automatically redirects all standard user traffic to secure Port 443.*

#### 1. Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

#### 2. Configure Nginx Base
```bash
sudo nano /etc/nginx/sites-available/synora
```
Paste the following (Replace `yourdomain.com` with your actual domain):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/synora /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

#### 4. Generate SSL & Auto-Redirect (Certbot Exemption)
Run Certbot. It will generate the SSL certificates and rewrite your Nginx file to redirect all Port 80 HTTP traffic to HTTPS, while keeping a hidden exemption for future 90-day renewals.
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
*(When prompted, select the option to automatically redirect all HTTP traffic to HTTPS).*

#### 5. Open Oracle Firewalls
Open port 443 (HTTPS) and port 80 (for the Certbot automated renewals):
```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```
> **CRITICAL:** Go to your Oracle Cloud Dashboard -> **Networking -> Virtual Cloud Networks -> Default Security List**, and add an **Ingress Rule** for Port `80` AND Port `443`.

---

### Option B: STRICT Port 443 Only (No Port 80 Allowed)
*Use this ONLY if strict corporate firewalls completely forbid opening Port 80. You will have to manually renew SSL via DNS every 90 days.*

#### 1. Generate SSL via DNS instead of HTTP:
```bash
sudo certbot certonly --manual --preferred-challenges dns -d yourdomain.com
```
*(Certbot will give you a TXT record. Add this TXT record to your domain's DNS settings to verify ownership).*

#### 2. Configure Nginx to Exclusively Listen on 443:
```bash
sudo nano /etc/nginx/sites-available/synora
```
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

#### 3. Open ONLY Port 443:
```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```
> **CRITICAL:** In the Oracle Cloud Dashboard, add an **Ingress Rule** for Port `443` ONLY.

---

**Deployment Complete!** 
You can now visit your fully encrypted, enterprise-grade deployed application by entering your domain in your browser: `https://yourdomain.com`
