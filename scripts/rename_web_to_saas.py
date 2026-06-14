# scripts/rename_web_to_saas.py
# Module containing functions: rename_web_to_saas.

import os
import shutil
from pathlib import Path

def rename_web_to_saas():
    root_dir = Path(__file__).parent.parent.resolve()
    web_dir = root_dir / "synora_saas"
    saas_dir = root_dir / "synora_saas"
    
    # 1. Rename physical folder
    if web_dir.exists():
        print(f"Renaming directory {web_dir.name}/ -> {saas_dir.name}/")
        shutil.move(str(web_dir), str(saas_dir))
    
    # 2. Rename entry points inside the new saas directory
    moves = [
        (saas_dir / "synora_saas.py", saas_dir / "synora_saas.py"),
        (saas_dir / "synora_saas.spec", saas_dir / "synora_saas.spec"),
        (saas_dir / "resources_synora_saas", saas_dir / "resources_synora_saas")
    ]
    for src, dst in moves:
        if src.exists():
            print(f"Renaming file/folder {src.name} -> {dst.name}")
            shutil.move(str(src), str(dst))

    # 3. Global Find-and-Replace
    replacements = {
        "from synora_saas.routes": "from synora_saas.routes",
        "from synora_saas.core": "from synora_saas.core",
        "import synora_saas.routes": "import synora_saas.routes",
        "import synora_saas.core": "import synora_saas.core",
        "synora_synora_saas/synora_saas.py": "synora_synora_saas/synora_saas.py",
        "synora_synora_saas/synora_saas.spec": "synora_synora_saas/synora_saas.spec",
        "resources_synora_saas": "resources_synora_saas",
        "synora_saas.py": "synora_saas.py",
        "synora_saas.spec": "synora_saas.spec",
        "synora_saas/": "synora_saas/",
        "synora_saas\\\\": "synora_saas\\\\"
    }
    
    # Be careful not to replace generic words indiscriminately, target Python imports and known paths
    
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
                
                # Careful ordered replacements
                for old_str, new_str in replacements.items():
                    new_content = new_content.replace(old_str, new_str)
                    
                # Specific build/path logic
                new_content = new_content.replace('"synora_saas"', '"synora_saas"')
                new_content = new_content.replace("'synora_saas'", "'synora_saas'")
                
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated references in {filepath.relative_to(root_dir)}")
                    files_modified += 1
            except Exception as e:
                pass # skip unreadable files
                
    print(f"\nRename Complete! Converted 'synora_saas' to 'synora_saas' across {files_modified} files.")

if __name__ == "__main__":
    rename_web_to_saas()
