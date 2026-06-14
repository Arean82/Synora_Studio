# Synora Studio

Welcome to **Synora Studio**! This repository hosts a highly modular, enterprise-grade AI chat ecosystem and RAG platform.

Synora Studio has undergone a massive architectural overhaul. To guarantee stability, security, and scalability, the monolithic application has been **decoupled into strictly isolated, standalone components**. 

There is no monolithic entry point. You must run, scale, and distribute each component entirely independently.

---

## 🚀 Getting Started (Quick Boot)

Since the architecture is strictly modular, you must start the **API Server** first so that the other modules have a backend to connect to. 

### Prerequisites
1. Ensure you have **Python 3.10+** installed.
2. Install all global dependencies from the root directory:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the `.env.example` file to `.env` in the root directory and configure your environment variables.

### Boot Sequence

**1. Start the API Server (Backend Core)**
```bash
python server/run_server.py
```
*(Note: When you run this for the first time, you will encounter the `CLI AUTHENTICATION GATE` prompt in your terminal. Please read the `/server/INSTALLATION.md` for a complete walkthrough of how to satisfy this prompt.)*

**2. Start the Web Portal (SaaS Frontend)**
```bash
python web/run_web.py
```

**3. Start the Desktop Client (Local Native App)**
```bash
python desktop/main.py
```

*(Note: The Companion Operation toolkit and the Universal Admin Credentials Resetter are on-demand utilities and do not need to be left running.)*

---

## 🏗️ Architecture & Detailed Installation Manuals

The platform is divided into primary modules. **Each module contains its own dedicated, highly detailed `INSTALLATION.md` manual for Windows and Linux.**

### 1. 🧠 API Server (`/server`)
The foundational centralized intelligence core.
- **Features:** Exposes REST gateways, handles LLM orchestration (OpenAI, Google GenAI, local Ollama endpoints), manages RAG ingestion pipelines, and semantic vector routing.
- **Setup Guide:** [server/INSTALLATION.md](server/INSTALLATION.md)

### 2. 🌐 Web Portal (`/web`)
A multi-tenant SaaS dashboard and administration portal that consumes the server backend.
- **Features:** User registration, usage accounting, BYOK (Bring Your Own Key) management, and OAuth integrations.
- **Setup Guide:** [web/INSTALLATION.md](web/INSTALLATION.md)

### 3. 🖥️ Desktop Client (`/desktop`)
A native desktop GUI application for end-users that wraps the core engine for native usage.
- **Features:** Connects to the local API Server, manages system prompts, chat history, and seamless AI interactions without browser overhead.
- **Setup Guide:** [desktop/INSTALLATION.md](desktop/INSTALLATION.md)

### 4. 🛠️ Companion Operation Toolkit (`/companion_operation`)
The primary administration toolkit for system administrators and DevOps engineers.
- **Features:** Automated SaaS database migrations, background service installation, automated backups, and restricted Web Platform Resets.
- **Setup Guide:** [companion_operation/INSTALLATION.md](companion_operation/INSTALLATION.md)

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
