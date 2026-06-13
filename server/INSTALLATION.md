# Synora Studio Server - Installation Manual

This is the standalone API server component of Synora Studio. It operates entirely independently to provide REST gateways and RAG processing.

## Requirements
- Python 3.10+
- `requirements.txt` dependencies

## Setup
1. Open a terminal in this `server` directory.
2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
## Running the Server

To start the API server and headless orchestrator, run:
```bash
python run_server.py
```

## Configuration
The API binds to port `5000` by default. It manages the local vector databases and orchestrates all cross-client communications.
