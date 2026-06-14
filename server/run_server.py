# server/run_server.py
# Module containing functions: run_headless_server.

import sys
import os
import time

# Add the root directory to sys.path so 'server' and 'desktop' modules resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_headless_server():
    from server.utils.logger import AppLogger
    logger = AppLogger.get_instance("server")
    logger.info("Starting isolated backend server...")
    
    from server.logic.llm_client import LLMClient
    client = LLMClient()
    client.hydrate()
    
    # 1. Start API Manager (Pure Headless Daemon)
    from server.logic.api_manager import ApiManager
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
    run_headless_server()
