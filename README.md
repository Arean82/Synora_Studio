# Synora Studio (v1.0.0 Initial Release)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)  ![PySide6](https://img.shields.io/badge/PySide6-6.11%2B-green)  ![OpenAI Compatible](https://img.shields.io/badge/OpenAI-Compatible-412991) ![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76B900) ![Google Gemini](https://img.shields.io/badge/Google-Gemini-8E75C2) ![Groq](https://img.shields.io/badge/Groq-LPU-F55036) ![Ollama](https://img.shields.io/badge/Ollama-Local-000000) ![LM Studio](https://img.shields.io/badge/LM%20Studio-Offline-6A0DAD) ![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-D92C2F) ![Turso](https://img.shields.io/badge/Turso-000000?style=flat&logo=turso&logoColor=cyan) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![License](https://img.shields.io/badge/License-GPLv3-blue)

A sleek, high-performance desktop chat application built with Python and PySide6. Designed as a universal multi-ecosystem hub, it interfaces seamlessly with **Google Gemini**, **NVIDIA NIM**, **Groq**, **Ollama**, and **LM Studio**—alongside infinite support for your own custom local endpoints—to provide unified streaming, blazing-fast markdown rendering, and enterprise-grade conversation management.

[About](#-about-the-project) • [Features](#-features) • [User Interface Highlights](#-user-interface-highlights) • [Getting Started](#-getting-started) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Tech Stack](#-tech-stack) • [Universal API Server](#-universal-api-server) • [Log System](#-log-system) • [Keyboard Shortcuts](#-keyboard-shortcuts) • [Credits](#-about-the-team--credits) • [License](#-license)

---

## 📖 About the Project

**Synora Studio** is engineered to be the definitive, secure gateway for modern Artificial Intelligence exploration. Developed for high-velocity prototyping and native desktop comfort, this workstation utility centralizes fragmented AI provider landscapes into a single, performant orchestrator.

Born from the drive for a truly ecosystem-agnostic environment, it breaks vendor-lock constraints by unifying **Cloud inference** and **Local compute** within one elite codebase. Leveraging hardware acceleration, OS-level credential custody, and recursive Adaptive Memory buffering, it delivers a fluid, virtually limitless conversational cognition engine.

---

## ✨ Features

- ☁️ **SaaS Multi-Tenant Gateway:** An enterprise-grade web orchestration layer supporting Admin Vault and BYOK (Bring Your Own Key) tiers. Features real-time telemetry, Dead Letter Queues (DLQ), live worker metrics, and physical tenant isolation.
- 🤖 **Hermes Autonomous Agent:** Seamlessly integrates autonomous background agents into the tenant sandbox, featuring omnichannel messaging connections (e.g., Telegram) and centralized persistent memory loops tied directly to the tenant's BYOK credentials.
- ✨ **Premium Glassmorphic UI:** Stunning 4K visual design featuring dynamic glowing gradients, micro-animations, and seamless Dark/Light theme switching for both the Desktop and Web environments.
- ⚔️ **AI Model Arena:** Brand-new competitive benchmark engine. Run dual LLMs concurrently side-by-side with real-time visual comparison, blind-mode evaluation, and victory elections.
- 🧬 **Hybrid Vector RAG Memory:** Deep long-term recollections. Synthesizes high-velocity NumPy TF-IDF crawls with industrial-grade, local Qdrant Vector Database storage for persistent semantic retrieval.
- 🛠️ **Interactive Python Sandbox:** Secure, decoupled execution environment. Spawns fully-isolated processes to automatically compile and execute generated Python and PySide GUI codebases safely on your desktop.
- ⚡ **Zero-Config Auto-Sweep:** Automated discovery of Ollama and LM Studio servers. A non-blocking, isolated background sweeper intelligently probes local ports to sync offline libraries with zero user configuration.
- 🤖 **Scalable Architecture (v1.0.0):** Advanced modular chassis natively supporting hot-swappable viewports across **Google**, **NVIDIA**, **Ollama**, **LM Studio**, **Groq**, and **Official OpenAI**.
- 🎛️ **Dynamic Capability-Based Filtering:** Intelligently filter models by **General Chat**, **Supports Tools**, **Vision/Multimodal**, **Embeddings**, **Rerankers**, or **Audio/Voice** using a unified, re-ordered UI filter that prioritizes active conversational models first.
- 📂 **Universal Model Cataloging:** Dynamically auto-classifies and indexes non-chat models from API endpoints during background fetches. The chat selection popup remains cleanly partitioned (strictly showing chat-capable models), while specialized layers (Embeddings, Rerankers, Audio) are cataloged for backend integrations.
- 🔍 **Pluggable Two-Stage Reranking Pipeline:** Maximizes code context and prompt grounding precision. Pairs candidate retrieval (Top 20) with high-recall cross-encoder rerankers (Local BGE / Cloud Cohere / Custom OpenAPI-compatible endpoints), featuring Hybrid A Structural Code Bias (scoring class/def blocks higher) and Hybrid B Diversity MMR (Maximal Marginal Relevance) overlap pruning.
- ➕ **Unlimited Custom Endpoints:** Dynamically inject custom, private, or locally-hosted model hosts into your roster without writing a single line of code.
- 🏠 **True Offline Capability:** Specialized zero-key mode automatically detects local tooling (like Ollama), bypassing verification blockers entirely.
- 📊 **Live Performance Metrics:** Track AI speed with real-time stats (Time to First Token, Tokens/sec, and usage usage) displayed beautifully after every response.
- 📎 **File Attachments:** Upload code (`.py`, `.js`), text, or data files directly into the chat for instant analysis.
- 🔐 **Centralized Credential Hub:** Unified single-pane-of-glass management for all API keys, base URLs, and ecosystems. Features SDK-to-Ecosystem mapping and isolated OS-level vault storage (Audit ID 046).
- 🛡️ **Hardened Settings Hub:** Addressed prototype pollution and XSS vulnerabilities in the settings interface by replacing raw HTML injections with strict DOM manipulation.
- 🛡️ **Secure Transition Gate:** Switching "Live" ecosystems now triggers a mandatory logout confirmation gate, preventing session leakage and ensuring clean state transitions (Audit ID 028).
- 🔄 **Background Model Fetching:** Smarter "Fetch Models" logic with ecosystem-aware background workers and real-time status telemetry (Audit ID 024).
- 🛡️ **Universal Key-Aware Filtering:** The UI automatically hides models from providers lacking active credentials, ensuring a zero-pollution catalog (Audit ID 047).
- ✨ **Premium Visual Identity:** Upgraded to a custom-generated 4K glassmorphism design with optimized assets for Windows (.ico), macOS (.icns), and Linux (.png) (Audit ID 018).
- 🔧 **Smart Tabbed Generation Parameters:** Take granular control over LLM outputs and RAG options through a beautiful, responsive tabbed interface. Tweak temperature, presets, and response lengths under "Model Parameters", and configure the dynamic two-stage reranker, endpoints, and secure API keys under "Retrieval Reranking".
- 🧠 **Reasoning Support:** Automatically detects and beautifully formats model "thinking/reasoning" tokens.
- 🎨 **Rich Markdown Rendering:** Stunning display of code blocks with syntax highlighting, tables, and bold formatting.
- 💾 **Robust History Management:** Uses a high-performance **Turso (libSQL)** backend with edge replication and **WAL (Write-Ahead Logging)** mode to ensure data integrity and prevent corruption, even during crashes or power loss.
- 🚅 **Instant Loading (HTML Cache):** Near-instant conversation loading thanks to an intelligent HTML caching system that pre-renders messages, bypassing heavy markdown parsing during UI refresh.
- 🔐 **State Memory:** Remembers your API keys, selected models, and theme preferences via `QSettings` (OS-native registry/config).
- 🖥️ **Distraction-Free UI:** Forced maximized, clean light/dark interface so you can focus purely on your prompt.
- 🌓 **Adaptive Theming** – Instantly switch between Dark and Light modes.
- 📌 **Persistent Settings** – API keys, models, and theme preferences survive app restarts.
- 🌐 **Live Connection Status** – Real-time network monitoring with visual indicators (🌐/🔴); automatically recovers from silent disconnects, safely cleans up broken chat history, and instantly unlocks the UI.
- 🛡️ **Intelligent Error Handling:** Categorizes API errors (timeouts, network drops, rate limits) and shows friendly, actionable messages instead of raw error traces.
- 🧠 **Adaptive Memory Compression:** Features a high-performance context intercept layer. Detects usage bursts above 85% and seamlessly performs silent, secondary background synthesis to compact legacy history, unlocking infinite conversation depth.
- 🔄 **Background Model Fetching:** Fetch and test all available ecosystem models in the background. Model Manager closes automatically, progress visible in real-time via the Log menu.
- 📋 **Real-time Log Viewer & Telemetry:** Track model fetching progress, API health, and system throughput with a centralized Telemetry Observability Dashboard.
- ✨ **AI-Powered Description Generation:** Generate one-sentence descriptions for any model using your choice of working model (Llama 4, Gemma 3, etc.). Descriptions persist across app restarts.
- 🏷️ **Developer Tabs:** Models are automatically grouped by developer (Google, Meta, NVIDIA, etc.) in the Model Manager for easier browsing.
- 💰 **Paid Model Support:** Fetch paid models (requires subscription) and merge them with existing free models without losing data.
- 🚀 **Graceful Resource Management:** Implements **Smart Resource Sync** and completely safe OS-level thread signaling (replacing unsafe termination) to guarantee absolute GUI state stability and memory integrity.
- 🖥️ **System Tray Support:** Minimize to system tray for background operation. API server continues running while app is in tray.
- 🌐 **Universal API Server:** Start a local OpenAI-compatible API server from Tools menu. Connect any IDE (VS Code, Eclipse, IntelliJ) to your selected LLM model.
- 🖥️ **VS Code Extension Support:** Use with Continue extension or build custom extension for advanced features like sending entire files, project folders, and applying AI edits directly.
- 📦 **Storage Management Center:** Move seamlessly between Portable, Standard, and Custom data paths at runtime with transactional relocation and immediate automatic cycle-boot.
- 📂 **Zero-Click Data Reveal:** Instant one-click Windows Explorer shortcuts in settings to navigate directly to your active user profiles and databases.
- 🧠 **Semantic Caching:** High-speed Jaccard Similarity matching for Semantic RAG caching, dramatically reducing token usage on identical semantic queries.

For detailed API documentation, see [API Documentation](API_SERVER.md)
For IDE integration instructions, see [IDE Integration Guide](IDE_INTEGRATION.md)

---

## 🎨 User Interface Highlights

### 🛠️ Operator Tools (Enterprise Utilities)

The application ships with isolated, administrative Operator Tools that execute completely outside the main process to ensure safety and bypass UI locks.

- **Operation Companion**: An automated database, web host/port, and configuration relocator tool. It safely migrates Turso/libSQL edge databases, Local offline blobs, Qdrant Vector Data, and user profiles across environments (Local to SaaS, or SaaS to Local), and manages network interface configurations.
- **Admin Reset Utility**: A specialized recovery tool designed to purge corrupted registries, wipe compromised API keys, and re-provision default Admin/Tenant databases without touching user chat history.

📂 **Browse the Full Gallery:** See more detailed interface caps in the [📂 resources/screenshots](./resources/screenshots) folder.

- 🌙 / ☀️ **Theme Toggle**: Click the icon in the top bar to switch themes instantly. The SaaS web portal now defaults to a premium Light Theme.
- 🏷️ **Model Info Label**: A subtle italic label next to the dropdown populates with the model description so you know its capabilities at a glance.
- 📋 **Log Menu:** View real-time update logs with filtering by log level. Clear logs when needed.
- ✨ **Generate Descriptions Button:** In Model Manager, select any working model to automatically generate descriptions for all models missing them.
- 📝 **System Instructions:** Access the Instruction Library via Settings to create, edit, and toggle system prompts.
- 🔽 **System Tray Icon:** Right-click for menu options, double-click to restore window from tray.
- **Universal API Server** - Start/stop local API server on port 5000. Checkmark indicates server is running. Compatible with any OpenAI-compatible IDE or plugin.

---

## 🌐 Network Port Configuration

Synora Studio utilizes the following default network ports:
- **Core Backend API Server**: Port `5000` (OpenAI-compatible local server).
- **SaaS Web Portal**: Port `8080` (Fully customizable via the **Operation Companion** GUI/CLI or directly in `saas/config.ini`).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- An API Key from your preferred provider (NVIDIA, Google, OpenAI etc.) (Get one at [build.nvidia.com](https://build.nvidia.com/))

### Installation

> **Note for macOS / Apple Silicon Users:** It is highly recommended to run `pip install pyside6` manually before installing the full requirements, as Apple Silicon occasionally struggles with Qt bindings depending on your Python environment.
> 
> **Note for ARM / Cloud IaaS Deployments:** If deploying headless to an Oracle Cloud VM (aarch64) or Raspberry Pi, please refer to **Section 8** of the [`HEADLESS_GUIDE.md`](file:///c:/Users/user/OneDrive/Desktop/python/synora_studio/HEADLESS_GUIDE.md) for critical OS-level dependencies required before running pip, and how to safely run Qdrant.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Arean82/synora_studio.git   
   cd synora_studio   
   ```
2. **Create and activate a virtual environment (Optional but recommended):**

   ```bash
   python -m venv venv   
   # Windows  
   venv\Scripts\activate   
   # macOS/Linux   
   source venv/bin/activate   
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt   
   ```

---

## 💡 Usage

1. Run the application:
   ```bash
   python main.py   
   ```
2. 🔑 **Secure Authentication Gate:** On startup, you will be greeted by the **Synora Admin Login Gateway**. Sign in with your Super Admin credentials (`admin` / `admin` by default). Your credentials are validated against the partitioned database layer.
3. 📸 **Dynamic Ecosystem Configuration:** If no ecosystem is active, the **Switch Ecosystem** dialog appears. Enter your API Key or select keyless local providers. Your keys are immediately encrypted using zero-trust PBKDF2 ciphers derived from your master password and securely stored in your OS keychain.
4. 🤖 **Select Model:** Click the chat model selector in the main window to choose from your active providers.
5. 💬 **Start Chatting:** Type your message. Press `Enter` to send, or `Shift+Enter` for a new line.
6. 📎 **Upload Files:** Click the attachment button to upload code/text for the AI to review.
7. ⏹️ **Stop Generation:** Click the red "Stop" button at any time to halt the response.
8. 🔽 **System Tray:** Click the X button to choose between exiting completely or minimizing to system tray. Double-click tray icon to restore window.
9. 🌐 **API Server:** Go to Tools → Universal API Server to start the API. Configure your IDE extension to use `http://localhost:5000/v1`. You can securely manage your active keys and toggle the server directly via the CLI by running `python main.py --api-manager`.

---

## 📁 Project Structure

```text
synora_studio/
│
├── master.py                       # 🚀 Global orchestrator entry point
├── synora_studio.spec              # PyInstaller spec for unified build
├── build_deb.sh                    # 📦 Linux DEB compile & bundler script
├── build_appimage.sh               # 📦 Linux AppImage compile & bundler script
├── build_mac.sh                    # 📦 macOS PKG installer compile script
├── build_all_plugins.bat           # 📦 Windows plugins compile & bundler script
├── build_all_plugins.sh            # 📦 Unix plugins compile & bundler script
├── README.md                       # 📖 Documentation
├── LICENSE                         # ⚖️ GPLv3 License
├── SECURITY.md                     # 🛡️ Security policy and vulnerability disclosure
├── API_SERVER.md                   # 📡 API documentation
├── IDE_INTEGRATION.md              # 🔌 IDE setup guide
├── requirements.txt                # 📦 Python dependencies
│
├── desktop/                        # 🖥️ Local Desktop GUI App
│   ├── main.py                     # 🚀 Desktop entry point
│   ├── desktop.spec                # PyInstaller spec - Desktop only
│   ├── headless/                   # 🖥️ Headless Mode Engine
│   │   ├── auth.py                 # 🔐 CLI-based authentication handler
│   │   ├── engine.py               # ⚙️ Headless lifecycle orchestrator
│   │   └── worker.py               # 🧵 Headless stream processor
│   ├── ui/                         # 🧩 Python View Controller logic
│   │   ├── main_window.py          # 🖥️ Host Shell Window & Stack Orchestration
│   │   ├── chat_view.py            # 💬 Dynamic drag-drop & sandbox pipeline logic
│   │   ├── arena_view.py           # ⚔️ Dual comparison duel viewport logic
│   │   ├── credential_manager.py   # 🔐 Secure OS-level auth vault logic
│   │   └── ...                     # Other view controllers
│   └── ui_designer/                # 🎨 Qt Designer UI layouts
│
├── server/                         # ⚙️ Core Application Engine & Local Server
│   ├── run_server.py               # 🚀 Standalone server entry point
│   ├── server.spec                 # PyInstaller spec - Server only
│   ├── logic/                      # ⚙️ Core processing and RAG pipeline
│   │   ├── storage_drivers/        # 🗃️ Pluggable DB Driver Architecture
│   │   ├── llm_client.py           # 🔌 Universal Multi-Ecosystem Orchestrator
│   │   ├── rag_manager.py          # 🧬 Hybrid Document Indexer
│   │   └── ...                     # Other engine logic
│   ├── utils/                      # 🛠️ Low-Level System Helpers
│   ├── workers/                    # 🧵 Non-blocking Background Daemons
│   │   ├── connection_worker.py    # 🌐 Socket-level internet ping listener
│   │   ├── model_fetch_worker.py   # 🔄 Ecosystem background parser & testers
│   │   └── ...                     # Other async workers
│   ├── resources/                  # 📦 Static assets & caches
│   ├── scratch/                    # 🧪 Dynamic scratch scripts & tools
│   └── vector_db/                  # 💾 Persistent Qdrant dense semantic retrieval
│
├── web/                            # 🌐 Synora Studio SaaS Web Portal
│   ├── app.py                      # 🛡️ Secure SaaS Gateway & Flask Server
│   ├── run_web.py                  # 🚀 Standalone web entry point
│   ├── web.spec                    # PyInstaller spec - Web only
│   ├── config.ini                  # ⚙️ SaaS configuration
│   ├── core/                       # ⚙️ Web Core & Config Management
│   │   ├── agent_manager.py        # 🤖 Hermes Agent background orchestrator
│   │   ├── tenant_db.py            # 🗄️ Multi-Tenant factory switchboard
│   │   └── launcher.py             # 🚀 Web worker pool launcher
│   ├── tenant_drivers/             # 🔌 Pluggable Multi-Backend Tenant Drivers
│   ├── static/                     # 🎨 Glassmorphism Styles & Assets
│   ├── templates/                  # 📐 Modular Portal UI Blueprints
│   └── saas_docs/                  # 📖 Role-Based SaaS documentation
│
├── operator_tools/                 # 🔧 Isolated Operator Admin Portfolio
│   ├── admin_reset/                # 🔐 Universal Master Password Reset
│   │   └── reset_admin.py          # MVC Controller entrypoint
│   └── companion/                  # 🔄 Standalone DB Relocator
│       └── companion_operation.py  # GUI + CLI/Headless Controller entrypoint
│
├── extensions/                     # 📦 IDE Extensions & Binaries
│   ├── binaries/                   # Compiled VSIX and ZIP plugins
│   ├── vscode-llm-chat/            # 💻 VS Code Extension (TypeScript)
│   └── jetbrains-llm-chat/         # 💻 JetBrains IntelliJ Extension (Kotlin)
│
└── scripts/                        # 🛠️ Setup & Development Scripts
```

---

## 🏛️ System Architecture

The application leverages a fully-isolated, multi-threaded modular chassis designed to support concurrent operations across multiple interfaces without database locking or UI freezing:

![Quantum Architecture Diagram](resources/arch_diagram.png)

### 🧱 Three-Tier Modular System Layout:

1. **Multi-Interface Clients Layer**:

   * **PySide6 Desktop GUI**: A highly responsive, multi-threaded workspace executing long-running network operations via background worker threads to ensure zero main-loop freezing.
   * **Terminal CLI**: A lightweight, interactive command-line interface equipped with direct streaming, model hot-swapping, and metadata commands.
   * **Local API + SaaS Gateway**: Local OpenAI-compatible API traffic uses a bearer gate; SaaS traffic uses passport/BYOK tenant authentication and dynamic resource isolation. IDE extensions can target either gateway.
2. **Core Orchestration Chassis**:

   * Anchored by `ServiceRegistry`, `ConversationService`, `AuthService`, `RAGService`, `StorageService`, `CacheService`, `TelemetryManager`, and `CircuitBreaker`. The older `ConversationManager` remains as the desktop history compatibility path and still routes through the same storage-driver family.
3. **High-Concurrency Pluggable Storage Tier**:

   * **libSQL / Turso Edge Shards (Default)**: Leverages lightweight Hranas edge replication and database-per-tenant sharding to support zero-locking remote transactional operations.
   * **PostgreSQL Cluster Engine**: Offers enterprise-grade multi-process concurrency, implementing raw row-level locking and Multi-Version Concurrency Control (MVCC).
   * **Local SQLite / metadata fallback**: Preserves zero-config desktop history, SaaS user metadata, and local recovery flows with WAL enabled.
   * **Isolated Multi-Tenant Sandbox**: Enforces tenant isolation across auth, settings/BYOK credentials, history routing, vector collections, background jobs, and cache tables.

---

## 🧱 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)       ![Qt](https://img.shields.io/badge/PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=black)       ![OpenAI](https://img.shields.io/badge/OpenAI_SDK-412991?style=for-the-badge&logo=openai&logoColor=white)       ![NVIDIA](https://img.shields.io/badge/NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)       ![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75C2?style=for-the-badge&logo=googlegemini&logoColor=white)       ![Turso](https://img.shields.io/badge/Turso-000000?style=for-the-badge&logo=turso&logoColor=cyan)       ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)       ![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

---

## ⚙️ Configuration & High-Concurrency Data Storage

This application does not use local `.env` files or plaintext config files for sensitive data.

To eliminate multi-process write-locking timeout crashes across simultaneous **GUI (Desktop)**, **CLI (Terminal)**, and **SaaS API (Port 5000)** connections, **SQLite has been 100% purged** from the primary engine. In its place, the application implements pluggable MVCC/cloud storage:

* **API Credentials:** Migrated away from plaintext. Securely injected into the OS vault subsystem using the Python `keyring` module (Windows Credential Manager / macOS Keychain).
* **UI Settings:** Layout preferences stored dynamically using `QSettings`.
  * **Portable Mode:** Saved to `settings.ini` in the application folder (zero system footprint).
  * **Standard/Custom Mode:* Saved securely via native OS configurations (Windows Registry, macOS plist, Linux conf).
* **Pluggable Storage Chassis**:
  * **Turso / libSQL (Default)**: Executes queries over Hranas transactions with edge-replicated cloud database-per-tenant sharding.
  * **PostgreSQL (Enterprise)**: Connects dynamically to remote/local PG clusters, implementing native row-level locks and MVCC.
* **Isolated Multi-Tenant Sandboxing**:
  Supports multiple concurrent registered users working in private "virtual sandboxes" (each acting like a separate virtual desktop app instance). Isolates history, metadata, and BYOK credentials via dynamic tenant sharded DB paths, isolated settings blocks, and JWT-authenticated session tokens.

---

## 🌐 Universal API Server

- Fully compatible with OpenAI-style API  `/v1/chat/completions` (used by IntelliJ plugin).
- Start from **Tools → Universal API Server** (✅ = running). Server runs on `http://localhost:5000`
- **Security & Key Management:** Manage your local API server in **Settings → Generation Parameters → API Credentials**. You can view, regenerate, or hard-disable your key (which securely shuts down the port). Changes in this tab are executed instantly with a live confirmation popup.

### Endpoints

| Endpoint                 | Method | Description                     |
| ------------------------ | ------ | ------------------------------- |
| `/health`              | GET    | Server status                   |
| `/v1/models`           | GET    | List model                      |
| `/v1/chat/completions` | POST   | OpenAI-compatible chat endpoint |

### VS Code Extension (V2.0.0)

Install `extension/vscode-llm-chat-2.0.0.vsix`:

1. VS Code Extensions (Ctrl+Shift+X)
2. Click "..." → "Install from VSIX..." and select the file.
3. Automatically prompts onboarding on load to configure dynamic server URL and secure passport keys.

### JetBrains Extension (V2.0.0)

Install `extension/jetbrains-llm-chat-2.0.0.zip`:

1. Open JetBrains IDE (IntelliJ, PyCharm, WebStorm, etc.) and go to Settings → Plugins.
2. Click the ⚙️ (gear) icon → "Install Plugin from Disk...".
3. Select the `.zip` file and restart the IDE.
4. Configure connection via IDE settings to connect to the Universal API Server.

### Other IDEs

Configure any OpenAI-compatible extension with:

- **URL:** `http://localhost:5000/v1`
- **API Key:** The dynamically generated token from your active session (viewable in Settings).

---

## 📋 Log System

The application features a comprehensive logging system for background operations:

- **Real-time Updates:** All fetch and generation progress appears instantly in the Log Viewer
- **Color-coded Levels:** INFO (green), SUCCESS (blue), WARNING (yellow), ERROR (red), DEBUG (purple)
- **Filterable:** Toggle specific log levels on/off
- **Persistent Storage:** Logs saved to `resources/update_log.txt` and survive app restarts
- **Background Operations:** Model fetching and description generation run without blocking the UI

---

## ⌨️ Keyboard Shortcuts

| **Key**                      | **Action**                                                  |
| :--------------------------------- | :---------------------------------------------------------------- |
| `Enter`                          | Send message                                                      |
| `Shift + Enter`                  | Insert new line                                                   |
| `F11`                            | Toggle true Fullscreen                                            |
| `Esc`                            | Exit true Fullscreen                                              |
| `Close button (X)` or `Alt+F4` | Shows exit options (Exit Application / Minimize to Tray / Cancel) |
| `Ctrl+Alt+S`                     | Toggle Universal API Server (if shortcut configured)              |
| `Ctrl+N`                         | New Conversation                                                  |
| `Ctrl+S`                         | Save Conversation                                                 |
| `Ctrl+L`                         | Load Conversation                                                 |
| `Ctrl+M`                         | Minimize to Tray                                                  |
| `Ctrl+Q`                         | Exit                                                              |
| `Ctrl+D`                         | Clear Chat                                                        |
| `Ctrl+Shift+C`                   | Copy Last Response                                                |

---

## 🤝 Contributing

Contributions, issues, and feature requests are highly welcome! Whether it's fixing a bug, improving the UI, or adding support for a new API, your help is appreciated.

To contribute:

1. **Fork** the Project
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the Branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

**Guidelines:**

- Please follow standard Python [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Keep the UI consistent with the current light/dark theme logic.
- If adding new API endpoints, ensure they are handled safely in the `logic/` folder without blocking the main UI thread.

---

## ⚠️ Disclaimer

This software is provided as-is, free of charge, for educational and personal use purposes.

- **AI Accuracy:** This application interfaces with third-party Large Language Models (LLMs). The developers of this application do not control, endorse, or guarantee the accuracy, completeness, or appropriateness of the AI-generated responses. AI models can produce incorrect, biased, or offensive content.
- **User Responsibility:** You are solely responsible for any prompts you submit and any outputs you rely on. Always verify critical information generated by AI.
- **API Usage:** This app interfaces with multiple third-party AI APIs (NVIDIA, Google, OpenAI, Ollama). You are responsible for managing your own API keys, adhering to NVIDIA's Terms of Service, and monitoring your own API usage limits and quotas.
- **No Liability:** The maintainers of this repository shall not be held liable for any damages, data loss, or issues arising from the use of this software.

---

## 🔨 Building from Source (Developer Guide)

If you want to build the distributable installers yourself, follow the OS-specific steps below.

*Note: You must build on the target OS (Windows builds for Windows, Mac builds for Mac, Linux builds for Linux).*

### Prerequisites

1. Install all core and build dependencies: `pip install -r requirements.txt`
2. Generate the required OS icon files from your source `resources/app_icon.png`:

   ```bash
   python -c "from PIL import Image; img = Image.open('resources/app_icon.png'); img.save('resources/app_icon.ico', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]); img.resize((256, 256)).save('resources/app_icon_linux.png'); print('Icons generated!')"
   ```

   *(Note: To generate the `.icns` for macOS, you must run `iconutil` on a Mac).*

### Step 1: Build the Executable (All OS)

Run this from the project root. The project includes three spec files for different build types:

```bash
# 1. Standard Builds (App Only)
pyinstaller LLM_Chat_App_onedir.spec
pyinstaller LLM_Chat_App_onefile.spec
pyinstaller LLM_Chat_App_mac.spec

# 2. Full Suite Builds (App + Operator Tools)
pyinstaller LLM_Chat_App_onedir_full.spec
pyinstaller LLM_Chat_App_onefile_full.spec
pyinstaller LLM_Chat_App_mac_full.spec
```

**Build outputs:**

- One-dir: `dist/LLM_Chat_dir/` (folder containing the executable and all dependencies)
- One-file: `dist/LLM_Chat_one_file/Synora Studio.exe` (single executable file)
- Full builds will simultaneously compile `Migration Companion` and `Reset Admin` into `dist/`.
- On first launch, the executable checks directory permissions. If running from a restricted system folder (like `C:\Program Files`), it automatically creates data resources inside `AppData` to ensure zero-crash operation.
- If run from a writable folder (USB drive/Desktop), it prompts the user to select between **Portable**, **Standard**, or **Custom** storage paths.
- Uses **Smart Sync** to safely unpack current UI versions to the active Data Root without wiping user configs.

**Test the executable** before proceeding to package it!

### Step 2: Create the OS Installer

#### 🪟 Windows (Inno Setup)

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php).
2. Place `installer_script.iss` in the project root folder.
3. Open the `installer_script.iss` file in Inno Setup.
4. Go to **Build > Compile** (or press `Ctrl+F9`).
5. *Output:* `installer_output/Synora_Studio_Setup_v1.0.0.exe`

The installer copies the entire `dist/LLM_Chat_dir/` folder to `Program Files` and creates desktop/start menu shortcuts.

#### 🐧 Linux (DEB & AppImage)

For Ubuntu/Debian, use the automated build scripts:

**1. Create a DEB Installer:**

```bash
# Build onedir first
pyinstaller synora_studio.spec
# Run the automation script
bash build_deb.sh
# Install
sudo dpkg -i synorastudio_1.0.0.deb
```

**2. Create a Portable AppImage:**

```bash
# Build onedir first
pyinstaller synora_studio.spec
# Run the AppImage script
bash build_appimage.sh
```

Uninstall DEB: `sudo apt remove synorastudio`

#### 🍎 macOS (PKG)

For macOS (Intel & Apple Silicon M1/M2/M3/M4), use the automated build script:

```bash
# Build mac bundle first
pyinstaller LLM_Chat_App_mac.spec
# Run the automation script
bash build_mac.sh
```

The compiled app leverages a dynamic configuration manager on the first boot to determine file locations:

1. **Standard Mode:** Installs configurations to the standard secure User Home location (e.g., `~\LLMChatApp`). Perfect for standard installations.
2. **Truly Portable Mode:** Packs absolutely every single byte—including SQL databases, caches, and even the settings files—into the same folder as the `.exe`. Safe for thumb drives.
3. **Custom Mode:** Routes all data folders to a network drive or synchronized folder of the user's choosing (e.g., Dropbox/OneDrive).

Regardless of selection, the target root directory will structure itself like this:

- `/conversations/` - SQLite database `chat_history.db`
- `/vector_db/` - Local persistent semantic vector databases (Qdrant)
- `/resources/` - Extracted styling and JSON manifests
- `/resources/badge_cache/` - Dynamic cached images
- `/ui_designer/` - Extracted interface schemas
- `/resources/update_log.txt` - Global application log file

---

## 👨‍💻 About the Team & Credits

This framework is architected and curated with the vision of building transparent, universal gates into advanced AI technologies.

* **Lead Architect:** **Arean Narrayan** ([@Arean82](https://github.com/Arean82))
* **Design Ethos:** Deliver highly secure, agnostic interfaces free of platform bias or maintenance decay.

---

## 📅 Change Log

### v1.0.0 – Initial Release

* **Initial Release**: Synora Studio v1.0.0 brings a unified AI ecosystem orchestrator with a highly modular architecture, local and cloud model support, advanced multi-tenant SaaS capabilities, and a robust offline/headless execution mode.

---

## 📝 License

This project is licensed under the GNU General Public License v3.0 (GPLv3) - see the [LICENSE](LICENSE) file for details.
