# server_script.py
# Isolated entry point for the Synora Studio API Server

import sys
import os

# Explicitly ensure we only load local server resources, breaking root dependencies
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from run_server import main
except ImportError:
    from server.run_server import main

if __name__ == "__main__":
    print("Initializing Isolated Server Component...")
    main()
