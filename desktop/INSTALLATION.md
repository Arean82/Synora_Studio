# Synora Studio Desktop - Installation Manual

This is the standalone Desktop GUI client of Synora Studio. It connects to the standalone API server.

## Requirements
- Python 3.10+
- `requirements.txt` dependencies

## Setup
1. Open a terminal in this `desktop` directory.
2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
3. Run the application:
   ```bash
   python desktop_script.py
   ```

## Important
Ensure the API Server (`server_script.py`) is running on port 5000 before initiating the desktop client to ensure full functionality.
