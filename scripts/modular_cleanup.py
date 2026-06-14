# scripts/modular_cleanup.py
# Module containing functions: organize_workspace.

import os
import shutil
from pathlib import Path

def organize_workspace():
    # Since this script is now inside the 'scripts' folder, the root is the parent directory
    root_dir = Path(__file__).parent.parent.absolute()
    
    print("Starting Synora Studio Modularization Cleanup...")

    # 1. Decentralize Documentation
    docs_dir = root_dir / "docs"
    
    doc_moves = {
        "API_SERVER.md": root_dir / "server" / "docs",
        "HEADLESS_GUIDE.md": root_dir / "server" / "docs",
        "USER_MANUAL_SAAS.md": root_dir / "web" / "docs",
        "SAAS_STORAGE_ARCHITECTURE_PLAN.md": root_dir / "web" / "docs",
        "USER_MANUAL_DESKTOP.md": root_dir / "desktop" / "docs",
        "IDE_INTEGRATION.md": root_dir / "extensions" / "docs",
    }
    
    print("\n--- Decentralizing Documentation ---")
    for doc_name, target_folder in doc_moves.items():
        src = docs_dir / doc_name
        if src.exists():
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(target_folder / doc_name))
            print(f"Moved {doc_name} -> {target_folder.relative_to(root_dir)}/")
        elif (root_dir / doc_name).exists():
            # Fallback if they are still in root
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(root_dir / doc_name), str(target_folder / doc_name))
            print(f"Moved {doc_name} -> {target_folder.relative_to(root_dir)}/")

    # 2. Organize Build Scripts
    build_dir = root_dir / "build_scripts"
    build_dir.mkdir(exist_ok=True)
    
    scripts_to_move = [
        "build_all_plugins.bat",
        "build_all_plugins.sh",
        "build_appimage.sh",
        "build_deb.sh",
        "build_mac.sh",
        "installer_script.iss"
    ]
    
    print("\n--- Moving Build Scripts ---")
    for script in scripts_to_move:
        src = root_dir / script
        if src.exists():
            shutil.move(str(src), str(build_dir / script))
            print(f"Moved {script} -> build_scripts/")

    # 3. Remove Deprecated Monolithic Files
    files_to_delete = [
        "synora_studio.spec",
        "modular_cleanup.py", # Add the incorrectly placed script to the cleanup list
        "scratch_recover.py", # Remove scratch files to obey single py file rule
        "run.py"              # Remove run.py as requested by user to perfectly clean the root
    ]
    
    print("\n--- Removing Deprecated Monolithic Files ---")
    for f in files_to_delete:
        src = root_dir / f
        if src.exists():
            os.remove(src)
            print(f"Deleted {f}")

    # 4. Remove Redundant Wrapper Scripts & Obsolete Modules
    print("\n--- Removing Redundant/Obsolete Files ---")
    wrappers_to_delete = [
        "web/web_script.py",
        "server/server_script.py",
        "desktop/desktop_script.py",
        "companion_operation/core/local_relocator.py",
        "companion_operation/ui_assets/local_relocator.ui"
    ]
    for w in wrappers_to_delete:
        src = root_dir / w
        if src.exists():
            try:
                os.remove(src)
                print(f"Deleted redundant wrapper: {w}")
            except Exception as e:
                print(f"Could not delete {w}: {e}")

    # 5. Remove Migrated JSON Files
    import glob
    print("\n--- Removing Migrated JSON Configurations ---")
    json_targets = []
    
    # Check resources dir for models files (api_providers.json is STATIC and MUST NOT BE DELETED)
    resources_dir = root_dir / "resources"
    if resources_dir.exists():
        json_targets.append(resources_dir / "models.json")
        json_targets.extend(list(resources_dir.glob("models_*.json")))
        json_targets.extend(list((resources_dir / "models").glob("models_*.json")))
        
    for j_path in json_targets:
        if j_path.exists():
            try:
                os.remove(j_path)
                print(f"Purged migrated JSON: {j_path.name}")
            except Exception as e:
                print(f"Could not purge {j_path.name}: {e}")

    # 6. Distribute Resources
    print("\n--- Distributing Shared Resources ---")
    if resources_dir.exists():
        targets = {
            "web/resources_web": "web",
            "desktop/resources_desktop": "desktop",
            "server/resources_server": "server",
            "companion_operation/resources_comp": "companion",
            "admin_reset/resources_rest": "reset"
        }
        
        for rel_path, name in targets.items():
            dest = root_dir / rel_path
            # Avoid copying into itself if mistakenly run from within resources
            if not dest.exists():
                try:
                    shutil.copytree(str(resources_dir), str(dest))
                    print(f"Copied resources to {rel_path}")
                except Exception as e:
                    print(f"Failed to copy to {rel_path}: {e}")
            else:
                print(f"Skipped {rel_path} (already exists)")
                
        all_exist = all((root_dir / path).exists() for path in targets.keys())
        if all_exist:
            try:
                shutil.rmtree(str(resources_dir))
                print("Deleted global monolithic resources folder.")
            except Exception as e:
                print(f"Could not delete global resources: {e}")
                
    operator_dir = root_dir / "operator_tools"
    if operator_dir.exists():
        try:
            shutil.rmtree(str(operator_dir))
            print("Deleted operator_tools directory as requested.")
        except Exception as e:
            print(f"Could not delete operator_tools: {e}")

    # 7. Documentation Cleanup: Remove localized translations
    print("\n--- Documentation Cleanup: Purging Translations ---")
    
    localized_files = ["README_de.md", "README_es.md", "README_fr.md"]
    
    # Recursive delete of translated READMEs
    for root_dir_path, dirs, files in os.walk(root_dir):
        # Skip git or build dirs
        if ".git" in root_dir_path or "__pycache__" in root_dir_path:
            continue
        for file in files:
            if file in localized_files:
                target_file = Path(root_dir_path) / file
                try:
                    os.remove(target_file)
                    print(f"Purged localized docs: {target_file.relative_to(root_dir)}")
                except Exception as e:
                    print(f"Could not delete {file}: {e}")

    print("\n✅ Cleanup Complete! The root directory is now strictly modularized.")
    print("Documentation translations have been purged.")

if __name__ == "__main__":
    organize_workspace()
