import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.logic.llm_client import LLMClient
from headless.cli.auth import HeadlessAuth

if __name__ == "__main__":
    print("[*] Starting Headless CLI Client...")
    client = LLMClient()
    client.hydrate()
    HeadlessAuth.run_login_flow(client)
    print("[+] API Configured. Ready to send requests to the API Server at port 5000.")
