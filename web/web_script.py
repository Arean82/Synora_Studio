# web_script.py
# Isolated entry point for the Synora Studio Web Portal

import sys
import os

# Explicitly ensure we only load local web resources, breaking root dependencies
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from run_web import main
except ImportError:
    from web.run_web import main

if __name__ == "__main__":
    print("Initializing Isolated Web Component...")
    main()
