# Synora Desktop Client (`/desktop`)

The Desktop Client is the native Graphical User Interface (GUI) for the Synora Studio ecosystem. Built with PyQt6, it offers a seamless, high-performance window into the AI capabilities powered by the isolated API Server.

## 🚀 Quick Setup
Please refer to the detailed [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on how to install and boot the desktop app for local use.

## 🏗️ Core Responsibilities

1. **Native OS Integration:** Interfaces directly with the OS to provide system tray integration, native notifications, and secure keychain access (`keyring`).
2. **Local AI Interaction:** Provides the UI for chatting with local Ollama endpoints or cloud providers via the `Socket.IO` streams provided by the API Server.
3. **Decoupled Connectivity:** The Desktop app does absolutely zero heavy lifting. It does not parse models, generate embeddings, or run RAG algorithms. It simply forwards UI interactions to the API server running on port `5000`.
4. **Configuration Management:** Handles the `.ini` / registry configuration files for user preferences (themes, font sizes, UI behaviors).

## 📚 Advanced Documentation

- [USER_MANUAL_DESKTOP.md](docs/USER_MANUAL_DESKTOP.md) - A comprehensive guide for end-users on how to navigate the desktop interface.
- [HEADLESS_INTEGRATION.md](headless/README.md) - Documentation on how the Desktop module allows the API server to temporarily hook into its security vault logic when booting headlessly.
