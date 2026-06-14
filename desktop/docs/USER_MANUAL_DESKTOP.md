# Synora Desktop Client: User Manual

Welcome to the **Synora Desktop Client**. This application gives you a native, lightning-fast window into the intelligence of your isolated backend API server.

## Getting Started

1. **Start the API Server:** Before opening the desktop app, ensure you have run `python server/run_server.py`. The desktop app cannot function without the backend running on port 5000.
2. **Launch the App:** Run `python desktop/main.py`.

## Core Features

### 1. Chat Interface
The primary view is your conversational interface. 
- You can seamlessly switch between AI Providers (e.g., OpenAI, Google Gemini, Ollama) using the drop-down menu in the top-right corner.
- **RAG (Retrieval-Augmented Generation):** Click the "Attach Document" button to seamlessly upload PDFs, Code files, or Text documents. The desktop client will securely transmit them to the API Server for chunking and semantic search indexing.

### 2. System Prompts
Customize your AI's persona and behavior.
- Click the **Agent Persona** button to define global instructions (e.g., "You are an expert Python developer. Never explain the code, just output the script.")

### 3. Security Vault & API Keys
Because Synora enforces a Bring-Your-Own-Key (BYOK) architecture, you must configure your API credentials locally.
- Navigate to **Settings (Gear Icon) -> Security Vault**.
- Enter your Provider API Keys.
- The Desktop App uses `cryptography.fernet` and your Operating System's native `keyring` to heavily encrypt these keys at rest. The plain text is never exposed, and keys are only transmitted locally to the API Server during active inference.
