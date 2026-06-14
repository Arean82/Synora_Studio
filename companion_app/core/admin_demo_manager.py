# companion_app/core/admin_demo_manager.py
# Module containing classes: AdminDemoManager, functions: is_demo_enabled, inject_demo_user, remove_demo_user.

from synora_server.logic.tenant.tenant_db import TenantDatabaseManager
from .ssh_tunnel import SSHTunnelManager
import json

class AdminDemoManager:
    @staticmethod
    def _execute_no_params(sql: str):
        SSHTunnelManager.setup_environment()
        db = TenantDatabaseManager()
        conn = db.get_connection()
        try:
            if hasattr(conn, 'cursor'):
                cur = conn.cursor()
                cur.execute(sql)
                if sql.strip().upper().startswith("SELECT"):
                    return cur.fetchone()
            else:
                res = conn.execute(sql)
                if sql.strip().upper().startswith("SELECT"):
                    return res.fetchone()
            if hasattr(conn, 'commit'):
                conn.commit()
        finally:
            if hasattr(conn, 'close'):
                conn.close()
        return None

    @staticmethod
    def is_demo_enabled() -> bool:
        res = AdminDemoManager._execute_no_params("SELECT id FROM users WHERE username = 'demo'")
        return res is not None

    @staticmethod
    def inject_demo_user():
        if AdminDemoManager.is_demo_enabled():
            return False, "Demo user is already enabled."
            
        SSHTunnelManager.setup_environment()
        db = TenantDatabaseManager()
        api_key = "demo_passport"
        pwd = "demo"
        
        user_id, err, _ = db.register_user(api_key, "demo", "demo@grid.net", pwd)
        if err:
            return False, err
            
        # Bypass OTP for demo
        try:
            settings = {"otp_verified": True}
            db.update_user_settings(user_id, settings)
            return True, f"Demo user injected successfully. (Username: demo, Password: {pwd})"
        except Exception as e:
            return False, f"Demo created but failed to bypass OTP: {e}"

    @staticmethod
    def remove_demo_user():
        try:
            AdminDemoManager._execute_no_params("DELETE FROM users WHERE username = 'demo'")
            return True, "Demo user removed successfully."
        except Exception as e:
            return False, str(e)
