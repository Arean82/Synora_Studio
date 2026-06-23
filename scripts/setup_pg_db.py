import os
import sys
from pathlib import Path
import psycopg2
import getpass
import configparser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Ensure synora_server is in PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

def provision_databases():
    print("==================================================")
    print("  Synora Studio: PostgreSQL Database Provisioning")
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

    print(f"\n[Configuration Loaded from config.ini]")
    print(f"Target User: {target_user}")
    print(f"SaaS Database: {saas_db}")
    print(f"Chat Database: {chat_db}")

    # 1. Connect to the local PostgreSQL server as the superuser
    try:
        print("\n[*] Connecting to local PostgreSQL server as 'postgres'...")
        pg_password = getpass.getpass("Enter password for superuser 'postgres': ")
        
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=pg_password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
    except Exception as e:
        print(f"[!] Failed to connect to PostgreSQL: {e}")
        return

    # 2. Create User Role
    print(f"\n[*] Ensuring role '{target_user}' exists...")
    try:
        cur.execute(f"CREATE USER {target_user} WITH PASSWORD '{target_password}';")
        print(f"    -> Role '{target_user}' created.")
    except psycopg2.errors.DuplicateObject:
        print(f"    -> Role '{target_user}' already exists.")
        # Update the password just in case it changed in config
        cur.execute(f"ALTER USER {target_user} WITH PASSWORD '{target_password}';")

    # 3. Create Databases
    databases = [saas_db, chat_db]
    for db in databases:
        print(f"[*] Ensuring database '{db}' exists...")
        try:
            cur.execute(f"CREATE DATABASE {db} OWNER {target_user};")
            print(f"    -> Database '{db}' created.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"    -> Database '{db}' already exists.")

    cur.close()
    conn.close()

    # 4. Initialize Schemas
    print("\n[*] Initializing Database Schemas via Native Drivers...")
    try:
        import urllib.parse
        encoded_user = urllib.parse.quote_plus(target_user)
        encoded_password = urllib.parse.quote_plus(target_password)

        # Initialize SaaS Tenant tables
        from synora_server.logic.tenant.drivers.postgres_tenant_driver import PostgresTenantDriver
        tenant_dsn = f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{saas_db}"
        print(f"    -> Initializing SaaS tables in {saas_db}...")
        PostgresTenantDriver(tenant_dsn)
        
        # Initialize Chat History tables
        from synora_server.logic.storage_drivers.postgres_driver import PostgreSQLStorageDriver
        chat_dsn = f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{chat_db}"
        print(f"    -> Initializing Chat History tables in {chat_db}...")
        PostgreSQLStorageDriver(chat_dsn)
        
        print("\n[+] SUCCESS! PostgreSQL is fully provisioned and schemas are ready.")
        print("[!] Next Steps:")
        print(f"    Run: python scripts/migrate_to_pg.py")
    except Exception as e:
        print(f"[!] Error initializing schemas: {e}")

if __name__ == "__main__":
    provision_databases()
