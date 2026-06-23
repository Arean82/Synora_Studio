# Synora Studio

Welcome to **Synora Studio**! This repository hosts a highly modular, enterprise-grade AI chat ecosystem and RAG platform.

Synora Studio has undergone a massive architectural overhaul. To guarantee stability, security, and scalability, the monolithic application has been **decoupled into strictly isolated, standalone components**. 

There is no monolithic entry point. You must run, scale, and distribute each component entirely independently.

### ✨ Key Features
- **Self-Learning Model Ranking**: Models are automatically sorted and ranked dynamically based on your usage frequency, pushing the most relevant models to the top of the Desktop and SaaS portals.

---

### System Requirements (Cloud Deployments)
If you are deploying Synora Studio on a headless Ubuntu Linux server (VPS) and wish to render the Desktop or Companion GUI natively via X11 Forwarding, install the following packages:
```bash
sudo apt update
sudo apt install xauth x11-apps libgl1-mesa-glx libegl1-mesa libxkbcommon-x11-0
```

## 🚀 Getting Started (Quick Boot)

Since the architecture is strictly modular, there is no monolithic entry point. You must boot the core backend first, and then launch your desired frontend client.

### 1. Start the API Server (Backend Core)
The API server must be running on Port 5000 before any client can function.
```bash
python server/server.py
```
*(Note: Upon first launch, you will encounter the `CLI AUTHENTICATION GATE`. Read `server/INSTALLATION.md` for details).*

### 2. Start your Frontend Client
Once the backend is active, launch one (or more) of the following interfaces:

**Desktop Client (Native GUI)**
```bash
python desktop/desktop.py
```

**Headless Client (Terminal CLI)**
```bash
python headless/headless.py --cli
```

**Web Portal (SaaS Dashboard)**
*(Listens on Port 8888 by default)*
```bash
python web/web.py
```

### 3. Administrator Operations
For DevOps tasks (DB Migrations, Password Resets), use the Companion App:
```bash
python companion_app/companion_app.py
```

---

## 🏗️ Architecture & Detailed Installation Manuals

The platform is divided into primary modules. **Each module contains its own dedicated, highly detailed `INSTALLATION.md` manual for Windows and Linux.**

### 1. 🧠 API Server (`/server`)
The foundational centralized intelligence core.
- **Features:** Exposes REST gateways, handles LLM orchestration (OpenAI, Google GenAI, local Ollama endpoints), manages RAG ingestion pipelines, and semantic vector routing. Contains the API Manager (`--api-manager`) CLI tool.
- **Setup Guide:** [server/INSTALLATION.md](server/INSTALLATION.md)

### 2. 🌐 Web Portal (`/web`)
A multi-tenant SaaS dashboard and administration portal that consumes the server backend.
- **Features:** User registration, usage accounting, BYOK (Bring Your Own Key) management, and OAuth integrations.
- **Setup Guide:** [web/INSTALLATION.md](web/INSTALLATION.md)

### 3. 🖥️ Desktop Client (`/desktop`)
A native desktop GUI application for end-users that wraps the core engine for native usage.
- **Features:** Pure PySide6 Graphical Interface. Connects to the local API Server, manages system prompts, chat history, and seamless AI interactions without browser overhead.
- **Setup Guide:** [desktop/INSTALLATION.md](desktop/INSTALLATION.md)

### 4. 🖧 Headless CLI Client (`/headless`)
A lightweight terminal-based interaction suite.
- **Features:** Fast interactive terminal chat (`--cli`), offline AI model synchronization (`--update-models`), and secure OS keychain credential entry.
- **Setup Guide:** [headless/INSTALLATION.md](headless/INSTALLATION.md)

### 5. 🛠️ Companion App Toolkit (`/companion_app`)
The primary administration toolkit for system administrators and DevOps engineers.
- **Features:** Unified Database Relocation (Chat DBs & SaaS Tenant DBs) via `--action migrate`, background service installation, automated backups, and Universal Admin Credentials Recovery (`--action reset-admin`).
- **Setup Guide:** [companion_app/INSTALLATION.md](companion_app/INSTALLATION.md)

---

## 🔒 Security Posture

Synora Studio enforces a strict security perimeter:
- **AES-GCM Encryption:** All external API Keys (BYOK) are encrypted at rest using `cryptography.fernet`.
- **Argon2id Hashing:** Password hashes use modern GPU-resistant key stretching.
- **Dynamic Authorization:** Local API server tokens are cryptographically generated and stored securely.
- **Email OTP 2FA:** Guest login flows utilize Time-based One-Time Passwords (TOTP) delivered asynchronously via email.

---

## 📚 Advanced Documentation
All legacy architectural plans, headless guides, and compilation manuals have been archived in the `/docs` directory. 
- Build scripts and PyInstaller pipelines are stored in `/build_scripts`.
- Deprecated monolithic files are safely archived in `/obsolete files`.
