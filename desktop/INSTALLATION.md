# Synora Studio Desktop - Installation Manual

This is the standalone Desktop GUI client of Synora Studio. It connects to the standalone API server.

## Requirements
- Python 3.10+
- `requirements.txt` dependencies

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

## Running the Desktop Client

To start the UI, run:
```bash
python main.py
```

## Important
Ensure the API Server (`run_server.py`) is running on port 5000 before initiating the desktop client to ensure full functionality.
