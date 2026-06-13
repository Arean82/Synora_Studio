# desktop_script.py
# Isolated entry point for the Synora Studio Desktop Client

import sys
import os

# Explicitly ensure we only load local desktop resources, breaking root dependencies
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from main import main
except ImportError:
    from desktop.main import main

if __name__ == "__main__":
    print("Initializing Isolated Desktop Component...")
    main()
