# desktop/core/auth_controller.py
# Module containing classes: AuthController, functions: run_gui_auth.

import sys

class AuthController:
    @staticmethod
    def run_gui_auth():
        from desktop.ui.user_login import UserLoginClass
        from desktop.ui.shared_widgets import set_app_icon
        
        login_dlg = UserLoginClass()
        set_app_icon(login_dlg)
        
        if not login_dlg.exec():
            print("[*] Admin login cancelled. Exiting.")
            sys.exit(0)
            
        from synora_server.logic.llm_client import LLMClient
        client = LLMClient()
        client.hydrate()
        
        # Ecosystem Check: If no provider is configured yet, show EcosystemSelector
        if not client.is_globally_authenticated():
            from desktop.ui.ecosystem_selector import EcosystemSelectorClass
            selector_dlg = EcosystemSelectorClass()
            set_app_icon(selector_dlg)
            
            if not selector_dlg.exec():
                print("[*] Ecosystem selection cancelled. Exiting.")
                sys.exit(0)
