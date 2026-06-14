# Synora Headless CLI Client (`/headless`)

The Headless CLI is a standalone terminal client for the Synora Studio ecosystem. It provides a lightweight, text-based interface to interact with the backend API Server without requiring the PyQt6 Desktop GUI or a web browser.

## 🚀 Quick Setup
Please refer to the [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on how to run the CLI and configure your AI Provider keys.

## 🏗️ Core Responsibilities

1. **CLI Authentication Gate:** The primary mechanism for users operating without a GUI to securely inject their API keys (e.g., OpenAI, Gemini) into the OS-level credential vault.
2. **Terminal Chat:** A text-based interactive loop allowing users to chat with AI models natively in their terminal.
3. **Decoupled Architecture:** The CLI does absolutely zero heavy lifting. It does not parse models or run RAG algorithms locally. It relies entirely on sending requests to the API Server running on port `5000`.

## 🔒 Security Posture

- When you enter an API key into the CLI, it is NOT saved in plaintext. 
- The CLI uses the Python `keyring` library to encrypt the keys directly into your operating system's native secure storage (such as Windows Credential Manager or the Linux Secret Service).
