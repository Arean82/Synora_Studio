# Oracle Cloud Ampere: Development Environment Manual

This guide is for configuring an Oracle Ampere A1 server strictly as a **Live Development Environment**. Instead of running compiled executables, the application is run directly from the raw Python source code using Virtual Environments. This allows developers connecting via the Antigravity IDE (VS Code Remote SSH) to edit code and test it instantly.

---

## Phase 1: Server Initialization & IDE Setup

### 1. Download the Codebase
We will place the code in a dedicated development directory to avoid confusing it with production environments.
```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv build-essential python3-dev \
                    libsecret-1-0 dbus-x11 gnome-keyring nginx

# Clone specifically to the Dev directory
git clone https://github.com/Arean82/Synora_Studio.git ~/Downloads/Synora_Studio
cd ~/Downloads/Synora_Studio
```

### 2. Configure Python Virtual Environment
Running from source requires a local Python virtual environment containing all dependencies.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Connect Antigravity IDE
At this point, use your local VS Code "Remote - SSH" extension (or your Antigravity client) to connect to the Oracle Ampere server. Open the `~/Downloads/Synora_Studio` folder directly in your IDE. You are now developing live on the server.

---

## Phase 2: Running the Development Servers

Since we are developing, we do NOT use `systemd` daemon services. We run the servers directly in the terminal so we can view the live console logs and test code changes dynamically.

### 1. Configure the Development Database
Before starting the servers, you must manually point the development environment to a database.
```bash
nano ~/Downloads/Synora_Studio/web/config.ini
```
Find the `[TENANT_DB]` section. Fill in your PostgreSQL database credentials (`pg_user`, `pg_password`, etc.).

> **No SQL Scripts Required!**
> The application will automatically run `CREATE TABLE IF NOT EXISTS` the moment you launch the server in the next step.

### 2. Start the API Server (Port 5001)
In an IDE terminal, activate the virtual environment and start the API:
```bash
cd ~/Downloads/Synora_Studio/server
source ../venv/bin/activate
python server.py --port 5001
```

### 2. Start the Web SaaS Portal (Port 8889)
In a *second* IDE terminal, start the Web Portal:
```bash
cd ~/Downloads/Synora_Studio/web
source ../venv/bin/activate
python web.py --port 8889
```

---

## Phase 3: Nginx SSL Reverse Proxy & Certbot

We need to securely expose these development ports to the internet using the `dev.synorastudio.in` domain. 

> **CRITICAL CONCEPT: How Certbot Handles Custom Ports**
> Certbot (`certbot --nginx`) automatically finds `listen 80;` blocks in Nginx, generates SSL certificates for those domains, and creates automated `listen 443 ssl;` blocks. 
> **Certbot completely ignores custom ports like 5001.** It will never automatically secure Port 5001. 
> Therefore, our strategy must be:
> 1. Configure the base HTTP traffic.
> 2. Run Certbot to generate the certificates.
> 3. *Then* manually create the Port 5001 server block and point it to the certificates Certbot just generated.

### Step A: Configure Base Nginx (Before Certbot)

Create the Dev Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/synoras-dev
```
Paste the following base configuration:
```nginx
# Web SaaS Portal Development (Proxies Port 443 -> 8889)
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

Enable it permanently and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/synoras-dev /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

> **Toggling the Dev Site**
> Since Nginx permanently routes traffic to Port 8889, you can completely control the availability of the site purely by running or stopping your Python scripts in the terminal:
> *   **Stop Development Site:** Press `Ctrl+C` in your terminal. Nginx will safely return a 502 Bad Gateway until you restart your script.

### Step B: Generate SSL Certificates (Run Certbot)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d dev.synorastudio.in
```
*(When prompted, select the option to automatically redirect all HTTP traffic to HTTPS).*

### Step C: Secure the Custom IDE API Port (Port 5001)
Now that Certbot has downloaded the SSL certificates to `/etc/letsencrypt/live/dev.synorastudio.in/`, we must manually inject them into a new Port 5001 block.

Open the Nginx file again:
```bash
sudo nano /etc/nginx/sites-available/synoras-dev
```
Paste this **new** block at the very bottom of the file:
```nginx
# Dedicated Visual Studio Native API Endpoint Development
server {
    listen 5001 ssl;
    server_name dev.synorastudio.in;

    # Manually point to the certificates Certbot generated in Step B
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
Restart Nginx one last time:
```bash
sudo systemctl restart nginx
```

---

## Phase 4: Oracle Firewall Requirements
Ensure your Oracle Cloud Dashboard Ingress rules allow Port 80, Port 443, and the new development Port **5001**.
```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5001 -j ACCEPT
sudo netfilter-persistent save
```

**Development Environment Ready!**
You can now edit code via IDE, view Web updates securely at `https://dev.synorastudio.in`, and connect your Visual Studio to the live API at `https://dev.synorastudio.in:5001`.
