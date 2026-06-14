# server/logic/settings_controller.py
# Module containing classes: SettingsController, functions: run_api_manager.

class SettingsController:
    @staticmethod
    def run_api_manager():
        print("[*] Initializing Local API Manager...")
        from server.utils.path_utils import get_app_settings
        import uuid
        settings = get_app_settings()
        
        while True:
            enabled = str(settings.value("api_enabled", "true")).lower() == "true"
            key = settings.value("local_api_auth_key", "")
            if not key:
                key = f"llm-local-auth-{uuid.uuid4().hex[:10]}"
                settings.setValue("local_api_auth_key", key)
            
            print("\n" + "="*50)
            print(" 🔌 LOCAL API MANAGER (Port 5000)")
            print("="*50)
            print(f" Status:  {'[ENABLED]' if enabled else '[DISABLED]'}")
            print(f" API Key: {key}")
            print("-" * 50)
            print(" 1. Toggle API (Enable/Disable)")
            print(" 2. Regenerate Key")
            print(" 3. Exit")
            print("="*50)
            
            choice = input("Select an action [1-3]: ").strip()
            
            if choice == "1":
                settings.setValue("api_enabled", "false" if enabled else "true")
                print(f"\n[*] API Server is now {'DISABLED' if enabled else 'ENABLED'}.")
                print("[*] (Restart the app or headless engine to apply network changes.)")
            elif choice == "2":
                new_key = f"llm-local-auth-{uuid.uuid4().hex[:10]}"
                settings.setValue("local_api_auth_key", new_key)
                print(f"\n[*] New Key Generated: {new_key}")
                print("[*] (Restart the app or headless engine to apply network changes.)")
            elif choice == "3":
                break
            else:
                print("\n[!] Invalid selection.")
