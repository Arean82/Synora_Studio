# companion_operation/core/ssh_tunnel.py
# Piggybacks off Desktop App QSettings to establish an SSH tunnel for remote database administration.

import os
from PySide6.QtCore import QSettings

class SSHTunnelManager:
    _tunnel = None
    _local_bind_port = None

    @staticmethod
    def get_desktop_config_path() -> str:
        comp_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Synora_Companion", "Companion_Config")
        return comp_settings.value("desktop_config_path", "")

    @staticmethod
    def start_tunnel_if_configured(remote_db_host: str, remote_db_port: int) -> int:
        """
        Reads the desktop app config, and if SSH is enabled, establishes a tunnel to the remote DB.
        Returns the local bind port (which might be the original port if SSH is disabled).
        """
        path = SSHTunnelManager.get_desktop_config_path()
        if not path:
            return remote_db_port  # No desktop config linked, assume local or direct connection

        # Look for the desktop config.ini
        ini_path = os.path.join(path, "config.ini")
        if not os.path.exists(ini_path):
            return remote_db_port

        # Read Desktop QSettings
        desktop_settings = QSettings(ini_path, QSettings.IniFormat)
        ssh_enabled = str(desktop_settings.value("ssh_enabled", "false")).lower() == "true"
        
        if not ssh_enabled:
            return remote_db_port
            
        ssh_host = str(desktop_settings.value("ssh_host", ""))
        ssh_port = int(desktop_settings.value("ssh_port", 22))
        ssh_user = str(desktop_settings.value("ssh_user", ""))
        
        ssh_pass_raw = str(desktop_settings.value("ssh_pass", ""))
        ssh_pass = ""
        try:
            import keyring
            if ssh_pass_raw == "KEYRING_STORED":
                ssh_pass = keyring.get_password("SynoraStudio", "ssh_pass") or ""
            elif ssh_pass_raw:
                import base64
                ssh_pass = base64.b64decode(ssh_pass_raw.encode()).decode()
        except ImportError:
            if ssh_pass_raw and ssh_pass_raw != "KEYRING_STORED":
                import base64
                ssh_pass = base64.b64decode(ssh_pass_raw.encode()).decode()

        ssh_key = str(desktop_settings.value("ssh_key", ""))
        
        ssh_key_pass_raw = str(desktop_settings.value("ssh_key_pass", ""))
        ssh_key_pass = ""
        try:
            import keyring
            if ssh_key_pass_raw == "KEYRING_STORED":
                ssh_key_pass = keyring.get_password("SynoraStudio", "ssh_key_pass") or ""
            elif ssh_key_pass_raw:
                import base64
                ssh_key_pass = base64.b64decode(ssh_key_pass_raw.encode()).decode()
        except ImportError:
            if ssh_key_pass_raw and ssh_key_pass_raw != "KEYRING_STORED":
                import base64
                ssh_key_pass = base64.b64decode(ssh_key_pass_raw.encode()).decode()
        
        if not ssh_host or not ssh_user:
            raise ValueError("SSH is enabled in Desktop config, but host or user is missing.")
            
        if not ssh_pass and not (ssh_key and os.path.exists(ssh_key)):
            raise ValueError("SSH requires either a valid password or a valid private key path.")
            
        try:
            import paramiko
            from sshtunnel import SSHTunnelForwarder
            
            kwargs = {
                "ssh_username": ssh_user,
                "remote_bind_address": (remote_db_host, remote_db_port),
                "local_bind_address": ('127.0.0.1', 0)
            }
            if ssh_pass:
                kwargs["ssh_password"] = ssh_pass
            if ssh_key and os.path.exists(ssh_key):
                kwargs["ssh_pkey"] = ssh_key
            if ssh_key_pass:
                kwargs["ssh_private_key_password"] = ssh_key_pass
                
            SSHTunnelManager._tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port),
                **kwargs
            )
            
            try:
                SSHTunnelManager._tunnel.start()
            except paramiko.ssh_exception.PasswordRequiredException:
                # Dynamically request passphrase if key is encrypted and no valid passphrase was saved
                import getpass
                print("\n[SECURITY] The SSH private key is encrypted and requires a passphrase.")
                interactive_pass = getpass.getpass("Enter SSH Key Passphrase: ")
                
                # Re-initialize the tunnel with the newly provided passphrase
                kwargs["ssh_private_key_password"] = interactive_pass
                SSHTunnelManager._tunnel = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    **kwargs
                )
                SSHTunnelManager._tunnel.start()
            SSHTunnelManager._local_bind_port = SSHTunnelManager._tunnel.local_bind_port
            return SSHTunnelManager._local_bind_port
        except ImportError:
            raise ImportError("Please install 'sshtunnel' and 'paramiko' to use secure piggybacking.")
        except Exception as e:
            raise RuntimeError(f"Failed to establish piggybacked SSH tunnel: {e}")

    @staticmethod
    def setup_environment():
        """
        Dynamically monkeypatches TenantDatabaseManager to route connections through the SSH Tunnel
        if a remote desktop config is present.
        """
        from synora_server.logic.tenant import tenant_db
        import re
        
        original_load = tenant_db._load_tenant_config
        
        def patched_load():
            cfg = original_load()
            
            if cfg["driver"] == "turso":
                return cfg # Local sqlite ignores ssh
                
            remote_host = "127.0.0.1"
            remote_port = 5432 if cfg["driver"] == "postgres" else cfg.get("mysql_port", 3306)
            
            if cfg["driver"] == "postgres":
                conn_str = cfg.get("pg_connection_string", "")
                m = re.search(r'@([^:/]+):(\d+)', conn_str)
                if m:
                    remote_host = m.group(1)
                    remote_port = int(m.group(2))
            else:
                remote_host = cfg.get("mysql_host", "127.0.0.1")
            
            # Start tunnel based on extracted remote DB host/port
            local_port = SSHTunnelManager.start_tunnel_if_configured(remote_host, remote_port)
            
            if SSHTunnelManager._tunnel:
                # Override config to point to the local bound port
                if cfg["driver"] == "postgres":
                    # Replace host:port with 127.0.0.1:local_port
                    new_conn = re.sub(r'@([^:/]+):(\d+)', f'@127.0.0.1:{local_port}', cfg["pg_connection_string"])
                    cfg["pg_connection_string"] = new_conn
                elif cfg["driver"] == "mysql":
                    cfg["mysql_host"] = "127.0.0.1"
                    cfg["mysql_port"] = local_port
                    
            return cfg
            
        tenant_db._load_tenant_config = patched_load

    @staticmethod
    def stop_tunnel():
        if SSHTunnelManager._tunnel:
            try:
                SSHTunnelManager._tunnel.stop()
            except:
                pass
            SSHTunnelManager._tunnel = None
            SSHTunnelManager._local_bind_port = None
