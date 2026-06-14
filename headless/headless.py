import sys
import os

# Resolve name shadowing by prioritizing the root project directory over the local script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

from server.logic.llm_client import LLMClient
from headless.cli.auth import HeadlessAuth

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("\n" + "="*50)
        print(" LLM CHAT APP - Headless CLI Client")
        print("="*50)
        print("Usage: python headless.py [options]")
        print("\nOptions:")
        print("  --cli             Launch the interactive terminal chat session")
        print("  --list-models     List all models currently in the local manifest")
        print("  --update-models   Fetch latest models from the active provider")
        print("  (no args)         Run Headless Authentication gate")
        print("="*50 + "\n")
        sys.exit(0)

    if "--list-models" in sys.argv:
        from headless.cli.models import HeadlessModels
        HeadlessModels.list_models()
        sys.exit(0)

    if "--update-models" in sys.argv:
        client = LLMClient()
        client.hydrate()
        from headless.cli.models import HeadlessModels
        HeadlessModels.update_models(client)
        sys.exit(0)

    if "--cli" in sys.argv:
        from headless.cli.chat_controller import ChatController
        ChatController.run_cli_chat()
        sys.exit(0)

    # Default action: run auth flow
    print("[*] Starting Headless CLI Client...")
    client = LLMClient()
    client.hydrate()
    HeadlessAuth.run_login_flow(client)
    print("[+] API Configured. Ready to send requests to the API Server at port 5000.")
