# companion_operation/core/admin_platform_reset.py
# Backend script for executing a highly restricted platform reset.

from synora_server.logic.tenant.tenant_db import TenantDatabaseManager
from .ssh_tunnel import SSHTunnelManager

class AdminPlatformReset:
    @staticmethod
    def _execute_no_params(sql: str):
        SSHTunnelManager.setup_environment()
        db = TenantDatabaseManager()
        conn = db.get_connection()
        try:
            if hasattr(conn, 'cursor'):
                cur = conn.cursor()
                cur.execute(sql)
            else:
                conn.execute(sql)
            if hasattr(conn, 'commit'):
                conn.commit()
        finally:
            if hasattr(conn, 'close'):
                conn.close()

    @staticmethod
    def execute_full_reset():
        """
        Executes a highly restricted backend script that safely drops all tenant data 
        from the server while preserving the master admin.
        """
        try:
            # Delete everyone except admin
            AdminPlatformReset._execute_no_params("DELETE FROM users WHERE username != 'admin'")
            return True, "Platform successfully reset. All non-admin tenants and their cascaded data have been wiped."
        except Exception as e:
            return False, f"Failed to reset platform: {str(e)}"
