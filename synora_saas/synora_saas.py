# synora_synora_saas/synora_saas.py
# Module containing functions: main.

import sys
import os

# Resolve name shadowing by prioritizing the root project directory over the local script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

from synora_saas.core.app import create_saas_app
from synora_server.utils.logger import AppLogger
from synora_server.logic.tenant.config_manager import SaaSConfigManager

def main():
    logger = AppLogger.get_instance("synora_saas")
    logger.info("Booting SaaS Web Portal in standalone mode...")
    
    config = SaaSConfigManager()
    host = config.get_str("NETWORK", "host", "127.0.0.1")
    port = config.get_int("NETWORK", "port", 8888)
    
    app = create_saas_app()
    print(f"[+] SaaS Web Portal is live. Listening on http://{host}:{port}...")
    
    try:
        from synora_saas.core.app import socketio
        # Run using SocketIO to support real-time WebSocket connections
        socketio.run(app, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Web Portal...")
    except Exception as e:
        logger.error(f"Web Portal Crash: {e}")
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
