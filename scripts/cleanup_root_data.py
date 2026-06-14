import os
import shutil
from pathlib import Path

def cleanup_root():
    root_dir = Path(__file__).parent.parent.resolve()
    
    # List of directories that were incorrectly generated in the project root
    rogue_dirs = [
        "data",
        "vector_db",
        "conversations"
    ]
    
    print(f"Scanning {root_dir} for rogue storage directories...")
    
    cleaned = False
    for rogue in rogue_dirs:
        target = root_dir / rogue
        if target.exists() and target.is_dir():
            print(f"Found rogue directory: {rogue}/ - Purging...")
            try:
                shutil.rmtree(target)
                print(f"✅ Successfully deleted {rogue}/")
                cleaned = True
            except Exception as e:
                print(f"❌ Failed to delete {rogue}/: {e}")
        elif target.exists() and target.is_file():
            print(f"Found rogue file: {rogue} - Purging...")
            try:
                target.unlink()
                print(f"✅ Successfully deleted {rogue}")
                cleaned = True
            except Exception as e:
                print(f"❌ Failed to delete file {rogue}: {e}")

    # Also clean up any loose config or db files dropped in the root
    rogue_files = [
        "saas_tenants.db",
        "saas_config.ini",
        "dlq.json",
        "telemetry_logs.jsonl"
    ]
    
    for rogue in rogue_files:
        target = root_dir / rogue
        if target.exists() and target.is_file():
            print(f"Found rogue file: {rogue} - Purging...")
            try:
                target.unlink()
                print(f"✅ Successfully deleted {rogue}")
                cleaned = True
            except Exception as e:
                print(f"❌ Failed to delete {rogue}: {e}")
                
    # Rescue orphaned saas configurations instead of deleting them
    saas_config = root_dir / "synora_saas" / "config.ini"
    saas_db = root_dir / "synora_saas" / "data" / "saas_tenants.db"
    server_data_dir = root_dir / "synora_server" / "data"
    
    if saas_config.exists() or saas_db.exists():
        server_data_dir.mkdir(parents=True, exist_ok=True)
        
    if saas_config.exists():
        print("Found orphaned synora_saas/config.ini - Rescuing to synora_server/data/config.ini")
        try:
            shutil.move(str(saas_config), str(server_data_dir / "config.ini"))
            cleaned = True
        except Exception as e:
            print(f"Failed to rescue config: {e}")
            
    if saas_db.exists():
        print("Found orphaned synora_saas/data/saas_tenants.db - Rescuing to synora_server/data/saas_tenants.db")
        try:
            shutil.move(str(saas_db), str(server_data_dir / "saas_tenants.db"))
            # Clean up the empty synora_saas/data directory if possible
            shutil.rmtree(str(root_dir / "synora_saas" / "data"), ignore_errors=True)
            cleaned = True
        except Exception as e:
            print(f"Failed to rescue db: {e}")
                
    if not cleaned:
        print("✅ Root directory is completely clean. No rogue files found.")
    else:
        print("✅ Cleanup complete. The modular workspace is pristine.")

if __name__ == "__main__":
    cleanup_root()
