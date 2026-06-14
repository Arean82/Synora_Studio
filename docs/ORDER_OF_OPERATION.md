# Synora Ecosystem: Order of Operation

Because Synora Studio operates on a strictly decoupled architecture, you cannot simply double-click a single file to boot the entire ecosystem. The modules rely on each other via API communication, meaning they must be started in a specific order.

## 🟢 1. The API Server (Mandatory)

The Server module is the central nervous system. It holds the LLM connections, processes the RAG chunking, and serves the SQLite tenant databases. **Nothing else will work if the server is offline.**

```bash
# Terminal 1
cd server
python run_server.py
```
*Wait until you see `[+] Backend Engine is live. Listening for API requests on Port 5000...` before proceeding to Step 2.*

## 🟡 2. Start a Client (Choose One)

Once the server is running silently in the background, you can connect to it using any of the available clients.

### Option A: The Web SaaS Portal (For Multi-Tenant Access)
```bash
# Terminal 2
cd web
python app.py
```
*The web portal will boot on port 8080 and communicate with the server on port 5000.*

### Option B: The Desktop GUI (For Native OS Experience)
```bash
# Terminal 2
cd desktop
python main.py
```
*The PyQt6 app will launch and communicate with the server on port 5000.*

### Option C: The Headless CLI (For Terminal Power Users)
```bash
# Terminal 2
cd headless
python run_cli.py
```
*The text-based chat interface will connect to the server on port 5000.*

## 🛑 3. Shutdown Sequence

To prevent database corruption and gracefully terminate all active LLM streams, shut down your clients first, and **shut down the server last** by pressing `Ctrl+C` in the server's terminal window.
