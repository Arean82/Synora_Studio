import os
from pathlib import Path

def purge_files():
    base_dir = Path(__file__).parent.parent / "synora_server" / "logic"
    files_to_delete = [
        base_dir / "tenant" / "drivers" / "turso_tenant_driver.py",
        base_dir / "tenant" / "drivers" / "mysql_tenant_driver.py",
        base_dir / "storage_drivers" / "libsql_driver.py",
        base_dir / "migration_bridge.py",
        Path(__file__).parent.parent / "companion_app" / "core" / "controller_saas_migrator.py"
    ]

    print("==================================================")
    print("  Synora Studio: Legacy Code Purge")
    print("==================================================")

    for file_path in files_to_delete:
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"[-] Deleted: {file_path.name}")
            except Exception as e:
                print(f"[!] Error deleting {file_path.name}: {e}")
        else:
            print(f"[ ] Already deleted: {file_path.name}")

    print("\n[+] Purge Complete.")

if __name__ == "__main__":
    purge_files()
