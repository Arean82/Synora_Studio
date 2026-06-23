import getpass
import psycopg2
import configparser
from pathlib import Path
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def delete_databases():
    print("==================================================")
    print("  Synora Studio: DROP PostgreSQL Databases")
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
    host = config["TENANT_DB"].get("pg_host", "localhost")
    port = config["TENANT_DB"].get("pg_port", "5432")
    saas_db = config["TENANT_DB"].get("pg_saas_db", "synora_saas")
    chat_db = config["TENANT_DB"].get("pg_chat_db", "synora_default_user")

    try:
        print("[*] Connecting to local PostgreSQL server as 'postgres'...")
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

    databases = [saas_db, chat_db]
    for db in databases:
        print(f"[*] Dropping database '{db}'...")
        try:
            # Disconnect other users if any before dropping
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{db}' AND pid <> pg_backend_pid();")
            cur.execute(f"DROP DATABASE IF EXISTS {db};")
            print(f"    -> Database '{db}' successfully deleted.")
        except Exception as e:
            print(f"    -> Error dropping '{db}': {e}")

    print(f"[*] Dropping role '{target_user}'...")
    try:
        cur.execute(f"DROP ROLE IF EXISTS {target_user};")
        print(f"    -> Role '{target_user}' successfully deleted.")
    except Exception as e:
        print(f"    -> Error dropping role: {e}")

    cur.close()
    conn.close()
    print("\n[+] Deletion complete. Your PostgreSQL server is clean.")

if __name__ == "__main__":
    delete_databases()
