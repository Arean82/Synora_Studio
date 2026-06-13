# Synora Studio Web - Installation Manual

This is the standalone web component of Synora Studio. It has been fully isolated and operates independently.

## Requirements
- Python 3.10+
- `requirements.txt` dependencies (`pip install -r requirements.txt`)

## Setup
1. Open a terminal in this `web` directory.
2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
   *(Note: The global requirements file is used for reference, but this module runs autonomously).*
3. Run the application:
   ```bash
   python web_script.py
   ```

## Configuration
The web portal binds to port `8888` by default. Environment variables can be injected via `config.ini` in this directory to alter SMTP relay or Turn/STUN server addresses.
