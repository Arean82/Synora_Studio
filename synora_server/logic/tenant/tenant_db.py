# synora_server/logic/tenant/tenant_db.py
# SaaS Multi-Tenant Database Factory Manager

"""
SaaS Multi-Tenant Database Factory Manager
Acts as a switchboard that manages the PostgreSQL SaaS Tenant connection.
Downstream callers never need to change.

Supported backends:
  - postgres — PostgreSQL via psycopg2
"""

import os
import urllib.parse
import configparser
import threading
from pathlib import Path


def _load_tenant_config() -> dict:
    """
    Reads the [TENANT_DB] section from synora_server/data/config.ini.
    """
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent.parent / "data" / "config.ini"
    if config_path.exists():
        config.read(str(config_path))
    
    result = {}
    if config.has_section("TENANT_DB"):
        user = config.get("TENANT_DB", "pg_user", fallback="synora")
        password = config.get("TENANT_DB", "pg_password", fallback="synora_secure_pw")
        host = config.get("TENANT_DB", "pg_host", fallback="localhost")
        port = config.get("TENANT_DB", "pg_port", fallback="5432")
        db = config.get("TENANT_DB", "pg_saas_db", fallback="synora_saas")
        
        encoded_user = urllib.parse.quote_plus(user)
        encoded_password = urllib.parse.quote_plus(password)
        
        result["pg_connection_string"] = f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{db}"
    else:
        result["pg_connection_string"] = "postgresql://synora:synora_secure_pw@localhost:5432/synora_saas"
    
    return result


class TenantDatabaseManager:
    """
    Factory switchboard for the SaaS tenant database.
    
    Delegates ALL method calls to the underlying PostgreSQL concrete driver instance.
    
    Usage:
        db = TenantDatabaseManager()
        user = db.authenticate_by_passport("my_api_key")
    """
    
    _thread_local = threading.local()
    
    def __new__(cls, db_name=None):
        """Thread-Local Singleton pattern — isolate DB connections per thread."""
        if not hasattr(cls._thread_local, 'instance'):
            cls._thread_local.instance = super().__new__(cls)
            cls._thread_local.instance._driver = cls._create_driver()
        return cls._thread_local.instance
    
    @classmethod
    def _create_driver(cls):
        """Factory method that instantiates the PostgreSQL driver."""
        config = _load_tenant_config()
        conn_str = config["pg_connection_string"]
        from synora_server.logic.tenant.drivers.postgres_tenant_driver import PostgresTenantDriver
        print(f"[TenantDB Factory] Loading PostgreSQL driver...")
        return PostgresTenantDriver(conn_str)

    # ------------------------------------------------------------------------
    # DELEGATION METHODS
    # ------------------------------------------------------------------------

    def __getattr__(self, name):
        """Delegate all missing attributes/methods to the underlying driver instance."""
        return getattr(self._driver, name)

    def force_reconnect(self):
        """Force the factory to drop the current connection and reload from config."""
        self._driver = self._create_driver()
        return True

