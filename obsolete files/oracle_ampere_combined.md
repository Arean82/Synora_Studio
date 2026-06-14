# Oracle Cloud Ampere: Combined Prod + Dev Manual

This is the ultimate master guide for running a **Live Production** environment (`synorastudio.in`) and an active **Development** environment (`dev.synorastudio.in`) simultaneously on the same Oracle Ampere A1 server, without conflicts or downtime.

---

## The Dual-Environment Architecture
To prevent collisions, the server is strictly partitioned into two logical zones:
| Environment | Domain | Source Directory | Web Port | IDE API Port | Execution Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Production** | `synorastudio.in` | `/opt/synora/bin/` | `8888` | `5000` | Compiled `systemd` Binaries |
| **Development** | `dev.synorastudio.in` | `~/Downloads/Synora_Studio/` | `8889` | `5001` | Raw Python Source via Terminal |

---

## Phase 1: Dual Directory Initialization

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv build-essential python3-dev \
                    libsecret-1-0 dbus-x11 gnome-keyring nginx \
                    nodejs npm default-jdk certbot python3-certbot-nginx
```

### 2. Clone Production and Development Zones
We will pull the codebase twice into distinct folders.
```bash
# Clone Production Codebase
git clone https://github.com/Arean82/Synora_Studio.git /home/ubuntu/Synora_Studio

# Clone Development Codebase
git clone https://github.com/Arean82/Synora_Studio.git ~/Downloads/Synora_Studio
```

### 3. Initialize the Development Zone
Set up the virtual environment so you can connect your Antigravity IDE natively:
```bash
cd ~/Downloads/Synora_Studio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
*You can now connect VS Code Remote SSH to `~/Downloads/Synora_Studio` and edit files live.*

---

## Phase 2: Deploy Production Zone

We must compile the production code and move it into the secure system `/opt` folder.

### 1. Compile the Executables
```bash
cd /home/ubuntu/Synora_Studio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

# Build IDE Plugins
bash build_all_plugins.sh

# Build Servers & Tools
cd server && pyinstaller server.spec && cd ..
cd web && pyinstaller web.spec && cd ..
cd operator_tools/admin_reset && pyinstaller reset_admin.spec && cd ../..
cd operator_tools/companion && pyinstaller companion_operation.spec && cd ../..
```

### 2. Move to Production Directory
```bash
sudo mkdir -p /opt/synora/bin/web
sudo chown -R ubuntu:ubuntu /opt/synora
sudo mkdir -p /var/log/synora
sudo chown -R ubuntu:ubuntu /var/log/synora

cd /home/ubuntu/Synora_Studio
cp server/dist/server/API_Server /opt/synora/bin/
cp web/dist/web/SaaS_Web_Portal /opt/synora/bin/
cp operator_tools/admin_reset/dist/operator_tools/Admin_Reset /opt/synora/bin/
cp operator_tools/companion/dist/operator_tools/Companion_Operation /opt/synora/bin/

cp -r extension/ /opt/synora/bin/
cp -r resources/ /opt/synora/bin/
cp -r web/locales/ /opt/synora/bin/web/
cp -r web/saas_docs/ /opt/synora/bin/web/
cp -r web/tenant_drivers/ /opt/synora/bin/web/
```

### 3. Generate Automated Production Services
```bash
sudo bash -c 'cat <<EOF > /opt/synora/bin/.env
QDRANT_URL=http://localhost:6333
DBUS_SESSION_BUS_ADDRESS=/dev/null
EOF'

cd /opt/synora/bin
# Generate and install API Service (Runs on 5000 by default)
echo -e "3\n2\nsynora-api\nSynora API Server\n1\nubuntu\nubuntu\non-failure\n5\n0\n/var/log/synora\n/opt/synora/bin/.env\ny\n6\n" | ./Companion_Operation --headless
sudo bash install_synora-api.sh

# Generate and install Web Service (Runs on 8888 by default)
echo -e "3\n2\nsynora-web\nSynora Web SaaS Portal\n1\nubuntu\nubuntu\non-failure\n5\n0\n/var/log/synora\n/opt/synora/bin/.env\ny\n6\n" | ./Companion_Operation --headless
sudo bash install_synora-web.sh
```
*Production is now fully running in the background!*

---

## Phase 3: Start the Development Zone

To test code changes, launch the uncompiled development servers from the terminal. 
**You must explicitly assign the development ports to avoid crashing the production servers!**

### 1. Launch Dev API Server (Port 5001)
In an IDE terminal:
```bash
cd ~/Downloads/Synora_Studio/server
source ../venv/bin/activate
python server.py --port 5001
```

### 2. Launch Dev Web Portal (Port 8889)
In a second IDE terminal:
```bash
cd ~/Downloads/Synora_Studio/web
source ../venv/bin/activate
python web.py --port 8889
```

---

## Phase 4: Modular Nginx & Multi-SSL Automation

We will route all traffic gracefully using Nginx. By using a **Modular Setup**, you can easily turn either environment on or off completely independently.

### Step A: Configure Production Nginx (`synoras`)
```bash
sudo nano /etc/nginx/sites-available/synoras
```
Paste the Production routing:
```nginx
# Production Web Portal (Proxies to 8888)
server {
    listen 80;
    server_name synorastudio.in www.synorastudio.in;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step B: Configure Development Nginx (`synoras-dev`)
```bash
sudo nano /etc/nginx/sites-available/synoras-dev
```
Paste the Development routing:
```nginx
# Development Web Portal (Proxies to 8889)
server {
    listen 80;
    server_name dev.synorastudio.in;

    location / {
        proxy_pass http://127.0.0.1:8889;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step C: Enable Nginx Routing Permanently
Enable both sites so Nginx is always ready to route traffic:
```bash
sudo ln -s /etc/nginx/sites-available/synoras /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/synoras-dev /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

> **How to Toggle Sites On and Off**
> You never need to touch Nginx symlinks again. Since Nginx just acts as a router, the site availability is controlled purely by the backend process.
> *   **To Turn OFF Production:** `sudo systemctl stop synora-web`
> *   **To Turn OFF Development:** Press `Ctrl+C` in your Dev terminal. Nginx will automatically return a `502 Bad Gateway` until you run the python script again.

### Step D: Run Certbot (Generate SSL)
Secure the domains by running Certbot for both modular files:
```bash
sudo certbot --nginx -d synorastudio.in -d www.synorastudio.in
sudo certbot --nginx -d dev.synorastudio.in
```
*(Select the option to automatically redirect all HTTP traffic to HTTPS).*

### Step E: Secure the IDE API Ports
Certbot has successfully generated your certificates. Now we must manually inject them into the custom IDE ports (Port 5000 and 5001) because Certbot ignores custom ports automatically.

**1. Secure Production Port 5000:**
```bash
sudo nano /etc/nginx/sites-available/synoras
```
Paste at the bottom:
```nginx
# Production Native API Endpoint
server {
    listen 5000 ssl;
    server_name synorastudio.in;

    ssl_certificate /etc/letsencrypt/live/synorastudio.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/synorastudio.in/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

**2. Secure Development Port 5001:**
```bash
sudo nano /etc/nginx/sites-available/synoras-dev
```
Paste at the bottom:
```nginx
# Development Native API Endpoint
server {
    listen 5001 ssl;
    server_name dev.synorastudio.in;

    ssl_certificate /etc/letsencrypt/live/dev.synorastudio.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dev.synorastudio.in/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

Restart Nginx one last time: `sudo systemctl restart nginx`

---

## Phase 5: CI/CD Pipeline (Code Promotion)

When you have tested a new feature on `dev.synorastudio.in` and want to push it to production without downtime:
1. `cd /home/ubuntu/Synora_Studio`
2. `git pull` (or copy the files from your Dev folder)
3. Run the specific PyInstaller `build.py` script to re-compile the binaries.
4. Copy the new executables over the old ones in `/opt/synora/bin/`.
5. Restart the production daemons: 
   ```bash
   sudo systemctl restart synora-api
   sudo systemctl restart synora-web
   ```

**Dual-Environment Server is now live and fully secured!**
