import os
import shutil
from pathlib import Path

def organize_workspace():
    # Since this script is now inside the 'scripts' folder, the root is the parent directory
    root_dir = Path(__file__).parent.parent.absolute()
    
    print("Starting Synora Studio Modularization Cleanup...")

    # 1. Organize Documentation
    docs_dir = root_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    docs_to_move = [
        "API_SERVER.md",
        "COMPILATION_MANUAL.md",
        "Enhancements_Planned.md",
        "HEADLESS_GUIDE.md",
        "IDE_INTEGRATION.md",
        "oracle_ampere_combined.md",
        "oracle_ampere_deployment.md",
        "oracle_ampere_development.md",
        "PROJECT_AUDIT_REPORT-old - ignore.md",
        "SAAS_STORAGE_ARCHITECTURE_PLAN.md",
        "SECURITY.md",
        "USER_MANUAL_DESKTOP.md",
        "USER_MANUAL_SAAS.md"
    ]
    
    print("\n--- Moving Documentation ---")
    for doc in docs_to_move:
        src = root_dir / doc
        if src.exists():
            shutil.move(str(src), str(docs_dir / doc))
            print(f"Moved {doc} -> docs/")

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
        "master.py",
        "synora_studio.spec",
        "modular_cleanup.py" # Add the incorrectly placed script to the cleanup list
    ]
    
    print("\n--- Removing Deprecated Monolithic Files ---")
    for f in files_to_delete:
        src = root_dir / f
        if src.exists():
            os.remove(src)
            print(f"Deleted {f}")

    # 4. Remove Redundant Wrapper Scripts
    print("\n--- Removing Redundant Wrapper Scripts ---")
    wrappers_to_delete = [
        "web/web_script.py",
        "server/server_script.py",
        "desktop/desktop_script.py"
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
    
    # Check resources dir for api_providers and models
    resources_dir = root_dir / "resources"
    if resources_dir.exists():
        json_targets.append(resources_dir / "api_providers.json")
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
            # Only remove if it's empty
            if not any(operator_dir.iterdir()):
                shutil.rmtree(str(operator_dir))
                print("Deleted empty operator_tools directory.")
        except Exception as e:
            pass

    print("\n✅ Cleanup Complete! The root directory is now strictly modularized.")
    print("Documentation has been moved to /docs and legacy build files to /build_scripts.")

if __name__ == "__main__":
    organize_workspace()
