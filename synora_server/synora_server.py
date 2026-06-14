# synora_server/synora_server.py
# Module containing functions: run_headless_server.

import sys
import os
import time

# Resolve name shadowing by prioritizing the root project directory over the local script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

def run_headless_server():
    from synora_server.utils.logger import AppLogger
    logger = AppLogger.get_instance("synora_server")
    logger.info("Starting isolated backend server...")
    
    from synora_server.logic.llm_client import LLMClient
    client = LLMClient()
    client.hydrate()
    
    # 1. Start API Manager (Pure Headless Daemon)
    from synora_server.logic.api_manager import ApiManager
    # Removed the request_handler_callback that was coupling the server to the Desktop engine
    api_manager = ApiManager(client)
    
    try:
        api_manager.start_api_server()
        print("[+] Backend Engine is live. Listening for API requests on Port 5000...")
        print("[+] Press Ctrl+C to terminate safely.")
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Termination signal received.")
    finally:
        print("[*] Cleaning up backend services...")
        api_manager.stop_api_server()
        print("[+] Shutdown complete.")

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("\n" + "="*50)
        print(" LLM CHAT APP - API Server Daemon")
        print("="*50)
        print("Usage: python server.py [options]")
        print("\nOptions:")
        print("  --api-manager     Manage the Local API Server (Port 5000) settings interactively")
        print("  (no args)         Start the background API server daemon")
        print("="*50 + "\n")
        sys.exit(0)

    if "--api-manager" in sys.argv:
        from synora_server.logic.settings_controller import SettingsController
        SettingsController.run_api_manager()
        sys.exit(0)

    run_headless_server()
