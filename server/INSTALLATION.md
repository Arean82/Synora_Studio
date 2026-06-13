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
3. Run the application:
   ```bash
   python server_script.py
   ```

## Configuration
The API binds to port `5000` by default. It manages the local vector databases and orchestrates all cross-client communications.
