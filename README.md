# Synora Studio

Welcome to **Synora Studio**! This repository hosts a highly modular, enterprise-grade AI chat ecosystem and RAG platform.

Synora Studio has undergone a massive architectural overhaul. To guarantee stability, security, and scalability, the monolithic application has been decoupled into three strictly isolated, standalone components. 

There is no longer a monolithic `master.py` entry point. Instead, you can run, scale, and distribute each component entirely independently, or use the unified `run.py` traffic controller.

### 🚀 Quick Start (Unified Entry Point)
If you prefer a single command, you can use the unified `run.py` in the root directory:
- **Desktop:** `python run.py`
- **Server:** `python run.py --server`
- **Web:** `python run.py --web`

---

## 🏗️ Architecture & Modules

The platform is divided into three primary modules. Each module contains its own dedicated execution script and `INSTALLATION.md` manual.

### 1. 🧠 API Server (`/server`)
The foundational centralized intelligence core.
- **Features:** Exposes REST gateways, handles LLM orchestration (OpenAI, Google GenAI, local Ollama endpoints), manages RAG ingestion pipelines, and semantic vector routing (Dual-Mode: `sentence-transformers` & Ollama). Runs completely independent of any UI.
- **Direct Source:** `python server/run_server.py`
- **Compiled Binary:** `./synora_server.exe`
- **Documentation:** `server/docs/HEADLESS_GUIDE.md`

### 2. 🌐 Web Portal (`/web`)
A multi-tenant SaaS dashboard and administration portal that consumes the server backend.
- **Features:** User registration, usage accounting, BYOK (Bring Your Own Key) management, and OAuth integrations.
- **Direct Source:** `python web/run_web.py`
- **Compiled Binary:** `./synora_web.exe`
- **Documentation:** `web/docs/USER_MANUAL_SAAS.md`

### 3. 🖥️ Desktop Client (`/desktop`)
A native desktop GUI application for end-users that wraps the core engine for native usage.
- **Features:** Connects to the local API Server, manages system prompts, chat history, and seamless AI interactions without browser overhead.
- **Direct Source:** `python desktop/main.py`
- **Compiled Binary:** `./Synora_Studio.exe`
- **Documentation:** `desktop/docs/USER_MANUAL_DESKTOP.md`



---

## 🔒 Security Posture

Synora Studio enforces a strict security perimeter:
- **AES-GCM Encryption:** All external API Keys (BYOK) are encrypted at rest using `cryptography.fernet`.
- **Argon2id Hashing:** Password hashes use modern GPU-resistant key stretching.
- **Dynamic Authorization:** Local API server tokens are cryptographically generated and stored securely in the SQLite database to prevent hardcoded secret leaks.
- **Email OTP 2FA:** Guest login flows utilize Time-based One-Time Passwords (TOTP) delivered asynchronously via email.

---

## 📚 Advanced Documentation
All legacy architectural plans, headless guides, and compilation manuals have been archived in the `/docs` directory. 
- Build scripts and PyInstaller pipelines are stored in `/build_scripts`.
- Deprecated monolithic files are safely archived in `/obsolete files`.

*Please refer to the `INSTALLATION.md` inside each module's respective folder to begin.*
