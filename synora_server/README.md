# Synora API Server (`/server`)

The API Server is the foundational intelligence core of the Synora Studio ecosystem. It operates entirely independently of any UI frontend. 

By running as a standalone module, it allows developers to build custom web, desktop, or mobile applications that simply consume its highly optimized REST and WebSocket endpoints.

## 🚀 Quick Setup
Please refer to the detailed [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on how to install dependencies, run the server, and pass the initial CLI Authentication Gate.

## 🏗️ Core Responsibilities

1. **LLM Orchestration:** Dynamically routes requests between local models (Ollama, LMStudio) and cloud providers (OpenAI, Google GenAI) via a unified `AgentManager`.
2. **Retrieval-Augmented Generation (RAG):** Manages the ingestion, chunking, and semantic searching of context files using dual-mode embeddings (`sentence-transformers` or remote models).
3. **Database Management:** Binds to the designated tenant database (SQLite, PostgreSQL, or libSQL/Turso).
4. **Multiplexing:** Handles high-concurrency event streams over `Flask-SocketIO` on port `5000`.

## 📚 Advanced Documentation

- [API_SERVER.md](docs/API_SERVER.md) - Detailed specifications of the REST routes and WebSocket event payloads.
- [HEADLESS_GUIDE.md](docs/HEADLESS_GUIDE.md) - Advanced documentation on deploying the server headlessly via Docker or Systemd, managing API key injection, and securing endpoints in production.
