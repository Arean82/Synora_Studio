# desktop/core/chat_controller.py
# Module containing classes: ChatController, functions: run_cli_chat.

import sys
import queue

class ChatController:
    @staticmethod
    def run_cli_chat():
        print("[*] Initializing interactive CLI Chat...")
        from server.logic.llm_client import LLMClient
        from desktop.headless.engine import HeadlessEngine
        from server.utils.path_utils import get_app_settings
        from server.logic.model_io import load_all_models
        
        client = LLMClient()
        client.hydrate()
        
        # 1. Initialize Headless Environment (CLI Auth + Manifest Sync)
        try:
            HeadlessEngine.ensure_initialized(client)
        except Exception as e:
            print(f"[!] CLI Setup Failed: {e}")
            return
            
        # 2. Resolve Active Model
        settings = get_app_settings()
        active_model = settings.value("current_model_id", "")
        models = load_all_models()
        if not active_model and models:
            active_model = models[0].get("id", "")
            settings.setValue("current_model_id", active_model)
            settings.sync()
            
        client.set_model(active_model)
        active_provider = client.get_current_provider()
        
        # 3. Interactive CLI Banner
        print("\n" + "="*80)
        print("  LLM CHAT APP - INTERACTIVE TERMINAL CHAT (CLI MODE)")
        print("="*80)
        print(f"  Active Provider: {active_provider.upper()}")
        print(f"  Active Model:    {active_model}")
        print("-" * 80)
        print("  Special Commands:")
        print("    /exit or /quit       - Exit interactive chat")
        print("    /list                - List all available models")
        print("    /model <model_id>    - Switch the active model")
        print("    /help                - Show this help message")
        print("="*80 + "\n")
        
        # 4. Interactive Chat Loop
        messages_history = []
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n[*] Exiting interactive chat.")
                break
                
            if not user_input:
                continue
                
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                if cmd in ("/exit", "/quit"):
                    print("[*] Exiting interactive chat.")
                    break
                elif cmd == "/list":
                    from desktop.headless.models import HeadlessModels
                    HeadlessModels.list_models()
                    continue
                elif cmd == "/model":
                    if len(parts) < 2:
                        print("[!] Usage: /model <model_id>")
                        continue
                    target_model = parts[1].strip()
                    from desktop.headless.models import HeadlessModels
                    if HeadlessModels.select_model(target_model):
                        client.set_model(target_model)
                        active_model = target_model
                        active_provider = client.get_current_provider()
                    continue
                elif cmd == "/help":
                    print("\nCommands:")
                    print("  /exit, /quit       - Terminate session")
                    print("  /list              - Show all recognized models")
                    print("  /model <model_id>  - Switch target model")
                    print("  /help              - Print commands roster\n")
                    continue
                else:
                    print(f"[!] Unknown command: {cmd}")
                    continue
            
            # Add user message to history
            messages_history.append({"role": "user", "content": user_input})
            
            # Start streaming worker
            q = queue.Queue()
            from desktop.headless.worker import HeadlessWorker
            
            worker = HeadlessWorker(
                client,
                messages_history,
                temperature=0.7,
                max_tokens=4096,
                on_chunk=lambda c: q.put(("chunk", c)),
                on_error=lambda e: q.put(("error", e)),
                on_finished=lambda: q.put(("finished", None))
            )
            worker.start()
            
            print("Assistant: ", end="", flush=True)
            full_response = ""
            while True:
                try:
                    event_type, val = q.get(timeout=0.1)
                    if event_type == "chunk":
                        print(val, end="", flush=True)
                        full_response += val
                    elif event_type == "error":
                        print(f"\n[!] Error: {val}")
                        break
                    elif event_type == "finished":
                        break
                except queue.Empty:
                    if not worker.is_alive():
                        break
            print() # end of line
            
            if full_response:
                messages_history.append({"role": "assistant", "content": full_response})
