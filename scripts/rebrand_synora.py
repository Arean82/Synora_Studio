# scripts/rebrand_synora.py
# Module containing functions: rebrand_synora.

import os
import shutil
from pathlib import Path

def rebrand_synora():
    root_dir = Path(__file__).parent.parent.resolve()
    
    server_old = root_dir / "synora_server"
    server_new = root_dir / "synora_server"
    
    saas_old = root_dir / "synora_saas"
    saas_new = root_dir / "synora_saas"
    
    # 1. Rename physical top-level folders
    if server_old.exists():
        print(f"Renaming directory {server_old.name}/ -> {server_new.name}/")
        shutil.move(str(server_old), str(server_new))
        
    if saas_old.exists():
        print(f"Renaming directory {saas_old.name}/ -> {saas_new.name}/")
        shutil.move(str(saas_old), str(saas_new))
        
    # 2. Rename internal core files
    core_moves = [
        # Server moves
        (server_new / "synora_server.py", server_new / "synora_server.py"),
        (server_new / "synora_server.spec", server_new / "synora_server.spec"),
        (server_new / "resources_synora_server", server_new / "resources_synora_server"),
        
        # SaaS moves
        (saas_new / "synora_saas.py", saas_new / "synora_saas.py"),
        (saas_new / "synora_saas.spec", saas_new / "synora_saas.spec"),
        (saas_new / "resources_synora_saas", saas_new / "resources_synora_saas"),
    ]
    
    for src, dst in core_moves:
        if src.exists():
            print(f"Renaming file/folder {src.name} -> {dst.name}")
            shutil.move(str(src), str(dst))

    # 3. Global Exact String Replacements
    replacements = {
        # Python Imports
        "from synora_server ": "from synora_server ",
        "from synora_server.": "from synora_server.",
        "import synora_server.": "import synora_server.",
        "from synora_saas ": "from synora_saas ",
        "from synora_saas.": "from synora_saas.",
        "import synora_saas.": "import synora_saas.",
        
        # Hardcoded Executable/File paths
        "synora_synora_server/synora_server.py": "synora_synora_server/synora_server.py",
        "synora_synora_saas/synora_saas.py": "synora_synora_saas/synora_saas.py",
        "synora_synora_server/synora_server.spec": "synora_synora_server/synora_server.spec",
        "synora_synora_saas/synora_saas.spec": "synora_synora_saas/synora_saas.spec",
        "resources_synora_server": "resources_synora_server",
        "resources_synora_saas": "resources_synora_saas",
        
        # File path substrings
        "synora_server/": "synora_synora_server/",
        "synora_saas/": "synora_synora_saas/",
        "synora_server\\\\": "synora_synora_server\\\\",
        "synora_saas\\\\": "synora_synora_saas\\\\",
        
        # Naked string literals in code (e.g. build scripts)
        '"synora_server"': '"synora_server"',
        "'synora_server'": "'synora_server'",
        '"synora_saas"': '"synora_saas"',
        "'synora_saas'": "'synora_saas'",
        
        '"synora_server.py"': '"synora_server.py"',
        "'synora_server.py'": "'synora_server.py'",
        '"synora_saas.py"': '"synora_saas.py"',
        "'synora_saas.py'": "'synora_saas.py'",
        
        '"synora_server.spec"': '"synora_server.spec"',
        "'synora_server.spec'": "'synora_server.spec'",
        '"synora_saas.spec"': '"synora_saas.spec"',
        "'synora_saas.spec'": "'synora_saas.spec'",
    }
    
    scan_dirs = ["synora_server", "synora_saas", "desktop", "companion_app", "extensions", "headless", "scripts", "operator_tools"]
    files_modified = 0
    
    for d in scan_dirs:
        scan_path = root_dir / d
        if not scan_path.exists():
            continue
            
        for filepath in scan_path.rglob("*"):
            if not filepath.is_file(): continue
            if filepath.suffix not in [".py", ".spec", ".md", ".sh", ".txt"]: continue
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                new_content = content
                for old_str, new_str in replacements.items():
                    new_content = new_content.replace(old_str, new_str)
                    
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated references in {filepath.relative_to(root_dir)}")
                    files_modified += 1
            except Exception as e:
                pass # skip unreadable files
                
    print(f"\nSynora Rebranding Complete! Updated links across {files_modified} files.")

if __name__ == "__main__":
    rebrand_synora()
