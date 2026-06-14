# synora_saas/synora_saas.py
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
        import os
        if os.name == 'nt':
            import ctypes
            def _win_handler(ctrl_type):
                print("\n[*] Kernel32 OS Intercept: Instant Kill...")
                os._exit(0)
                return True
            # Keep a local reference in main() to prevent garbage collection of the C callback
            _ctrl_handler = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)(_win_handler)
            ctypes.windll.kernel32.SetConsoleCtrlHandler(_ctrl_handler, True)
        else:
            import signal
            def force_exit(sig, frame):
                print("\n[*] OS Intercept: Force Shutting down Web Portal...")
                os._exit(0)
            signal.signal(signal.SIGINT, force_exit)
            signal.signal(signal.SIGTERM, force_exit)
        
        from synora_saas.core.app import socketio
        # Run using SocketIO to support real-time WebSocket connections
        socketio.run(app, host=host, port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Web Portal...")
        os._exit(0)
    except Exception as e:
        logger.error(f"Web Portal Crash: {e}")
        print(f"[!] Error: {e}")
        os._exit(1)

if __name__ == "__main__":
    main()
