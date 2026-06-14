# scripts/migrate_saas_core.py
# Module containing functions: migrate_saas_core.

import os
import shutil
from pathlib import Path

def migrate_saas_core():
    root_dir = Path(__file__).parent.parent.resolve()
    
    # Target Directories
    tenant_dir = root_dir / "synora_server" / "logic" / "tenant"
    drivers_dir = tenant_dir / "drivers"
    agents_dir = root_dir / "synora_server" / "logic" / "agents"
    
    tenant_dir.mkdir(parents=True, exist_ok=True)
    drivers_dir.mkdir(parents=True, exist_ok=True)
    agents_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Move Files
    moves = [
        (root_dir / "synora_saas" / "core" / "tenant_db.py", tenant_dir / "tenant_db.py"),
        (root_dir / "synora_saas" / "core" / "config_manager.py", tenant_dir / "config_manager.py"),
        (root_dir / "synora_saas" / "core" / "agent_manager.py", agents_dir / "agent_manager.py")
    ]
    
    # Add all tenant drivers
    old_drivers_dir = root_dir / "synora_saas" / "tenant_drivers"
    if old_drivers_dir.exists():
        for item in old_drivers_dir.iterdir():
            if item.is_file() and item.name.endswith(".py"):
                moves.append((item, drivers_dir / item.name))
                
    for src, dst in moves:
        if src.exists():
            print(f"Moving {src.relative_to(root_dir)} -> {dst.relative_to(root_dir)}")
            if dst.exists():
                dst.unlink() # remove if exists
            shutil.move(str(src), str(dst))
            
    # Clean up empty synora_saas/tenant_drivers folder
    if old_drivers_dir.exists():
        try:
            shutil.rmtree(str(old_drivers_dir))
            print("Removed empty synora_saas/tenant_drivers directory.")
        except Exception as e:
            print(f"Could not remove old drivers dir: {e}")

    # 2. Rewrite Imports
    replacements = {
        "server.logic.tenant.tenant_db": "server.logic.tenant.tenant_db",
        "server.logic.tenant.config_manager": "server.logic.tenant.config_manager",
        "server.logic.agents.agent_manager": "server.logic.agents.agent_manager",
        "server.logic.tenant.drivers": "server.logic.tenant.drivers",
        "from synora_server.logic.tenant import tenant_db": "from synora_server.logic.tenant import tenant_db",
        "from synora_server.logic.tenant import config_manager": "from synora_server.logic.tenant import config_manager",
        "from synora_server.logic.agents import agent_manager": "from synora_server.logic.agents import agent_manager"
    }
    
    scan_dirs = ["synora_server", "synora_saas", "desktop", "companion_app", "extensions", "headless", "scripts"]
    files_modified = 0
    
    for d in scan_dirs:
        scan_path = root_dir / d
        if not scan_path.exists():
            continue
            
        for filepath in scan_path.rglob("*.py"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                new_content = content
                for old_str, new_str in replacements.items():
                    new_content = new_content.replace(old_str, new_str)
                    
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated imports in {filepath.relative_to(root_dir)}")
                    files_modified += 1
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                
    print(f"\nMigration Complete! Surgically updated {files_modified} files.")

if __name__ == "__main__":
    migrate_saas_core()
