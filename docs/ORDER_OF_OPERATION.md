# Order of Operation & Architectural Flow

Synora Studio (v2.0) has been refactored into a strictly modularized system. This document outlines the explicit execution pathways, dependencies, and boot sequences for each primary component.

## 1. Server / Headless Engine (`server/`)
*The foundational API and backend orchestrator. Runs completely independent of any UI.*

**Execution:**
- **Direct Source:** `python server/run_server.py`
- **Compiled Binary:** `./synora_server.exe`

**Boot Sequence:**
1. **Init:** Loads environment variables and instantiates the core `AgentManager`.
2. **Database Binding:** Mounts to the active tenant database (libSQL/Turso, PostgreSQL, or local SQLite).
3. **Socket Binding:** Initializes the high-concurrency `Flask-SocketIO` multiplexer.
4. **Listener:** Begins listening on the designated API port (default: `5000`) for REST and WebSocket traffic. 

## 2. SaaS Web Portal (`web/`)
*The multi-tenant frontend interface that consumes the server backend.*

**Execution:**
- **Direct Source:** `python web/run_web.py`
- **Compiled Binary:** `./synora_web.exe`

**Boot Sequence:**
1. **Config Load:** Reads `config.ini` to determine port and active bindings.
2. **Mounting:** Dynamically mounts isolated route blueprints (`auth_routes.py`, `admin_routes.py`, `api_routes.py`, `dashboard_routes.py`).
3. **Worker Pool:** Spins up the isolated background worker pools via `launcher.py` to handle agentic reasoning loops without blocking the Flask UI.
4. **Listener:** Starts serving the glassmorphic web portal (default port: `8080`).

## 3. Desktop GUI (`desktop/`)
*The PySide6 native client that wraps the core engine for native usage.*

**Execution:**
- **Direct Source:** `python desktop/main.py`
- **Compiled Binary:** `./Synora_Studio.exe`

**Boot Sequence:**
1. **GUI Init:** Initializes the `QApplication` event loop.
2. **Authentication Gate (`auth_controller.py`):** Prompts the user for OS-level secure credentials or bypass logic.
3. **Settings Mount (`settings_controller.py`):** Loads the user's `QSettings` into the environment.
4. **Interface Load (`chat_controller.py`):** Mounts the PySide6 UI files and begins executing the main `QMainWindow` event loops.
5. **Worker Offload:** Passes all LLM generation streams to a `QThread` daemon to prevent UI lockup.

## 4. Unified Entry Point (`run.py` - Optional)
For convenience, `run.py` acts as a unified traffic controller in the root directory.

- `python run.py --server` routes to `server/run_server.py`
- `python run.py --web` routes to `web/run_web.py`
- `python run.py` (no flags) defaults to `desktop/main.py`
