# Oracle Cloud Enterprise Deployment & Compilation Manual

This is the complete, end-to-end production manual for deploying Synora Studio on an Oracle Cloud Ampere A1 server. 
It follows strict Linux production standards: compiling all modules, generating IDE plugins, placing binaries and resources in `/opt/synora`, managing them with automated `systemd` installers, and serving them securely through `Nginx`.

---

## Phase 1: Server Initialization
First, we acquire the codebase and prepare the Linux environment with required compilers, Node.js/Java for plugin compilation, and Docker for the vector database.

### 1. Download the Codebase
```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/Arean82/Synora_Studio.git
cd Synora_Studio
```

### 2. Install Native Dependencies, Plugins Toolchain & Nginx
```bash
sudo apt install -y python3-pip python3-venv build-essential python3-dev \
                    libsecret-1-0 dbus-x11 gnome-keyring nginx \
                    nodejs npm default-jdk
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
We will set up the build environment, bundle the IDE Plugins (VS Code & JetBrains), and compile the Python application modules into standalone Linux executables.

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

### 2. Compile IDE Extensions (VS Code & JetBrains)
```bash
# Generate the .vsix and .zip plugins into the extension/ directory
bash build_all_plugins.sh
```

### 3. Compile Core Servers
```bash
# Compile Backend API Server
cd /home/ubuntu/Synora_Studio/server
pyinstaller server.spec

# Compile Web SaaS Portal
cd /home/ubuntu/Synora_Studio/web
pyinstaller web.spec
```

### 4. Compile Operator Tools
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
A production server does not run executables out of a downloaded git repository. We will move the compiled binaries and their unbundled physical resources into the standard `/opt/` Linux directory.

### 1. Create Production Directories
```bash
sudo mkdir -p /opt/synora/bin/web
sudo mkdir -p /opt/synora/bin/server
sudo mkdir -p /var/log/synora
sudo chown -R ubuntu:ubuntu /opt/synora
sudo chown -R ubuntu:ubuntu /var/log/synora
```

### 2. Move Compiled Binaries & Unbundled Resources
Run these commands to move the 4 compiled executables and their required physical directories to the system folder:
```bash
cd /home/ubuntu/Synora_Studio

# Copy Core Binaries (Paths strictly derived from .spec files)
cp server/dist/server/API_Server /opt/synora/bin/
cp web/dist/web/SaaS_Web_Portal /opt/synora/bin/

# Copy Operator Tools (Paths strictly derived from .spec files)
cp operator_tools/admin_reset/dist/operator_tools/Admin_Reset /opt/synora/bin/
cp operator_tools/companion/dist/operator_tools/Companion_Operation /opt/synora/bin/

# Copy Missing IDE Extensions & App Resources
cp -r extension/ /opt/synora/bin/
cp -r resources/ /opt/synora/bin/

# Copy Missing Web Portal Resources (Translations, Drivers, Docs)
cp -r web/locales/ /opt/synora/bin/web/
cp -r web/saas_docs/ /opt/synora/bin/web/
cp -r web/tenant_drivers/ /opt/synora/bin/web/

# Ensure binaries are executable
chmod +x /opt/synora/bin/API_Server
chmod +x /opt/synora/bin/SaaS_Web_Portal
chmod +x /opt/synora/bin/Admin_Reset
chmod +x /opt/synora/bin/Companion_Operation
```

---

## Phase 4: Automated Service Deployment & DBus Fix
We will use the **Companion Operation** tool to automatically generate hardened, native Linux `systemd` services. We will also inject the DBus environment fix (`DBUS_SESSION_BUS_ADDRESS`) into the environment file to prevent `gnome-keyring` crashes on headless ARM environments.

### 1. Configure DBus and Qdrant Environment
```bash
# Create the environment file used by systemd
sudo bash -c 'cat <<EOF > /opt/synora/bin/.env
QDRANT_URL=http://localhost:6333
DBUS_SESSION_BUS_ADDRESS=/dev/null
EOF'
```

### 2. Configure the Production Database

Because the next step uses a headless deployment tool that bypasses the GUI database migration wizard, you must manually configure your database connection before starting the services.

```bash
sudo nano /opt/synora/bin/web/config.ini
```
Find the `[TENANT_DB]` section. Fill in your PostgreSQL database credentials (`pg_user`, `pg_password`, etc.).

> **No SQL Scripts Required!**
> You do *not* need to run any `.sql` initialization scripts. The Synora Studio drivers are programmed to run `CREATE TABLE IF NOT EXISTS` automatically. As soon as you start the application, it will scan your `config.ini` and automatically build the entire database schema for you.

### 3. Generate and Install Backend API Server Service
Run the companion tool in headless CLI mode and pipe the automation script to generate the API server installer script, then execute it.
```bash
cd /opt/synora/bin
echo -e "3\n2\nsynora-api\nSynora API Server\n1\nubuntu\nubuntu\non-failure\n5\n0\n/var/log/synora\n/opt/synora/bin/.env\ny\n6\n" | ./Companion_Operation --headless

# Run the generated bash installer script
sudo bash install_synora-api.sh
```

### 3. Generate and Install Web Portal Service
Run the companion tool again to generate and install the Web Portal daemon:
```bash
echo -e "3\n2\nsynora-web\nSynora Web SaaS Portal\n1\nubuntu\nubuntu\non-failure\n5\n0\n/var/log/synora\n/opt/synora/bin/.env\ny\n6\n" | ./Companion_Operation --headless

# Run the generated bash installer script
sudo bash install_synora-web.sh
```

---

## Phase 5: Nginx SSL Reverse Proxy & Certbot
We will use Nginx and Certbot to securely route HTTPS (Port 443) web traffic to the SaaS portal (Port 8888) and expose Port 5000 securely so Visual Studio 2022 can natively connect.

> **IMPORTANT PRE-REQUISITE:** Before continuing, you MUST purchase a domain name (e.g., `yourwebsite.com`) and point its DNS "A Record" to your Oracle Server's Public IP address.

### 1. Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Step A: Configure Base Nginx (Before Certbot)
```bash
sudo nano /etc/nginx/sites-available/synoras
```
Paste the following base configuration:
```nginx
# Web SaaS Portal (Proxies Port 443 -> 8888)
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

Enable it permanently and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/synoras /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

> **Toggling the Production Site**
> Since Nginx permanently routes traffic to Port 8888, you can completely control the availability of the site purely by starting or stopping the backend service:
> *   **Stop Production:** `sudo systemctl stop synora-web` and `sudo systemctl stop synora-api`
> *   **Start Production:** `sudo systemctl start synora-web` and `sudo systemctl start synora-api`

### Step B: Generate SSL Certificates (Run Certbot)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
*(When prompted, select the option to automatically redirect all HTTP traffic to HTTPS).*

### Step C: Secure the Custom IDE API Port (Port 5000)

Now that Certbot has downloaded the SSL certificates to `/etc/letsencrypt/live/yourdomain.com/`, we must manually inject them into a new Port 5000 block.

Open the Nginx file again:
```bash
sudo nano /etc/nginx/sites-available/synoras
```
Paste this **new** block at the very bottom of the file:
```nginx
# Dedicated Visual Studio Native API Endpoint
server {
    listen 5000 ssl;
    server_name yourdomain.com;

    # Manually point to the certificates Certbot generated in Step B
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```
Restart Nginx one last time:
```bash
sudo systemctl restart nginx
```

### 5. Open Oracle Firewalls
Open port 443 (HTTPS), port 80 (Certbot renewals), and port 5000 (Visual Studio IDE Integration):
```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo netfilter-persistent save
```
> **CRITICAL:** Go to your Oracle Cloud Dashboard -> **Networking -> Virtual Cloud Networks -> Default Security List**, and add an **Ingress Rule** for Port `80`, Port `443`, AND Port `5000`.

---

**Deployment Complete!** 
You can now visit your fully encrypted, enterprise-grade deployed application by entering your domain in your browser: `https://yourdomain.com` 
Visual Studio users can connect securely via `https://yourdomain.com:5000`.
