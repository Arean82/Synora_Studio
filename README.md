# Synora Studio

Welcome to **Synora Studio**! This repository hosts a highly modular, enterprise-grade AI chat ecosystem and RAG platform.

Synora Studio has undergone a massive architectural overhaul. To guarantee stability, security, and scalability, the monolithic application has been decoupled into three strictly isolated, standalone components. 

There is no longer a single global `master.py` entry point. Instead, you can run, scale, and distribute each component entirely independently.

---

## 🏗️ Architecture & Modules

The platform is divided into three primary modules. Each module contains its own dedicated execution script and `INSTALLATION.md` manual.

### 1. 🌐 Web Portal (`/web`)
A multi-tenant SaaS dashboard and administration portal.
- **Features:** User registration, usage accounting, BYOK (Bring Your Own Key) management, and OAuth integrations.
- **Entry Point:** `web/run_web.py`
- **Documentation:** [Web Installation Manual](web/INSTALLATION.md)

### 2. 🧠 API Server (`/server`)
The centralized intelligence core.
- **Features:** Exposes REST gateways, handles LLM orchestration (OpenAI, Google GenAI, local Ollama endpoints), manages RAG ingestion pipelines, and semantic vector routing (Dual-Mode: `sentence-transformers` & Ollama).
- **Entry Point:** `server/run_server.py`
- **Documentation:** [Server Installation Manual](server/INSTALLATION.md)

### 3. 🖥️ Desktop Client (`/desktop`)
A native desktop GUI application for end-users to interact with the LLMs.
- **Features:** Connects to the local API Server, manages system prompts, chat history, and seamless AI interactions without browser overhead.
- **Entry Point:** `desktop/main.py`
- **Documentation:** [Desktop Installation Manual](desktop/INSTALLATION.md)

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
