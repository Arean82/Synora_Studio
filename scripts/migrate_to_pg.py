import os
import sys
import configparser
from pathlib import Path

# Ensure synora_server is in PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

from synora_server.logic.migration_bridge import migrate_database, migrate_saas_tenant_database

def run_migration():
    print("==================================================")
    print("  Synora Studio: Turso to PostgreSQL Migration")
    print("==================================================")

    # 0. Read configuration from config.ini
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent / "synora_server" / "data" / "config.ini"
    if not config_path.exists():
        print(f"[!] config.ini not found at {config_path}")
        return
        
    config.read(config_path)
    if "TENANT_DB" not in config:
        print("[!] [TENANT_DB] section missing in config.ini")
        return
        
    target_user = config["TENANT_DB"].get("pg_user", "synora")
    target_password = config["TENANT_DB"].get("pg_password", "synora_secure_pw")
    host = config["TENANT_DB"].get("pg_host", "localhost")
    port = config["TENANT_DB"].get("pg_port", "5432")
    saas_db = config["TENANT_DB"].get("pg_saas_db", "synora_saas")
    chat_db = config["TENANT_DB"].get("pg_chat_db", "synora_default_user")
    
    import urllib.parse
    encoded_user = urllib.parse.quote_plus(target_user)
    encoded_password = urllib.parse.quote_plus(target_password)
    
    # ---------------------------------------------------------
    # 1. Migrate SaaS Tenant Data
    # ---------------------------------------------------------
    print("\n[Stage 1] Migrating SaaS Tenant Data (Users, Credentials, Orbits)...")
    try:
        from synora_server.logic.tenant.drivers.turso_tenant_driver import TursoTenantDriver
        from synora_server.logic.tenant.drivers.postgres_tenant_driver import PostgresTenantDriver
        
        source_tenant = TursoTenantDriver() # Automatically connects to saas_tenants.db via config
        dest_tenant = PostgresTenantDriver(f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{saas_db}")
        
        count = migrate_saas_tenant_database(
            source_driver=source_tenant, 
            dest_driver=dest_tenant, 
            progress_callback=lambda log: print(f"  -> {log}")
        )
        print(f"[+] SaaS Tenant Migration Complete! Moved {count} users.")
    except Exception as e:
        print(f"[!] Error migrating SaaS Tenants: {e}")

    # ---------------------------------------------------------
    # 2. Migrate Chat History for Default User
    # ---------------------------------------------------------
    print("\n[Stage 2] Migrating Local Chat History (Default User)...")
    try:
        from synora_server.logic.storage_drivers.libsql_driver import LibSQLStorageDriver
        from synora_server.logic.storage_drivers.postgres_driver import PostgreSQLStorageDriver
        
        # Determine local chat history SQLite path
        db_path = Path(__file__).parent.parent / "synora_server" / "data" / "conversations" / "chat_history.db"
        if not db_path.exists():
            print(f"  -> No local chat history found at {db_path}. Skipping.")
        else:
            source_storage = LibSQLStorageDriver(f"file:{db_path.as_posix()}", None)
            dest_storage = PostgreSQLStorageDriver(f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{chat_db}")
            
            conv_count = migrate_database(
                source_driver=source_storage, 
                dest_driver=dest_storage, 
                progress_callback=lambda log: print(f"  -> {log}")
            )
            print(f"[+] Chat History Migration Complete! Moved {conv_count} conversations.")
    except Exception as e:
        print(f"[!] Error migrating Chat History: {e}")

    print("\n==================================================")
    print("  Migration Process Finished!")
    print("  Verify your data in PostgreSQL. Once verified,")
    print("  we will proceed with Stage 2 (Codebase Purge).")
    print("==================================================")

if __name__ == "__main__":
    run_migration()
