# scripts/companion_merge_cleanup.py
# Module containing functions: main.

import os
import shutil
import sys

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    companion_old = os.path.join(root_dir, "companion_operation")
    companion_new = os.path.join(root_dir, "companion_app")
    admin_reset = os.path.join(root_dir, "admin_reset")

    print("Starting the companion_app and admin_reset merger cleanup...\n")

    # 1. Rename the main module directory
    if os.path.exists(companion_old):
        os.rename(companion_old, companion_new)
        print(f"Renamed: {os.path.basename(companion_old)} -> {os.path.basename(companion_new)}")
    elif not os.path.exists(companion_new):
        print(f"Error: Could not find {companion_old} or {companion_new}")
        sys.exit(1)

    # 2. Rename the main entry point
    old_entry = os.path.join(companion_new, "companion_operation.py")
    new_entry = os.path.join(companion_new, "companion_app.py")
    if os.path.exists(old_entry):
        os.rename(old_entry, new_entry)
        print("Renamed: companion_operation.py -> companion_app.py")

    # 3. Move core files
    core_files_to_move = ["reset_controller.py", "headless_reset.py"]
    for file in core_files_to_move:
        src = os.path.join(admin_reset, "core", file)
        dst = os.path.join(companion_new, "core", file)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved: {file} -> companion_app/core/")

    # 4. Move UI assets
    ui_src = os.path.join(admin_reset, "ui_assets", "reset_admin.ui")
    ui_dst = os.path.join(companion_new, "ui_assets", "reset_admin.ui")
    if os.path.exists(ui_src):
        shutil.move(ui_src, ui_dst)
        print("Moved: reset_admin.ui -> companion_app/ui_assets/")

    # 5. Delete the legacy admin_reset directory tree
    if os.path.exists(admin_reset):
        shutil.rmtree(admin_reset)
        print(f"Deleted: {os.path.basename(admin_reset)}/")

    print("\n✅ Merge Cleanup Complete! The unified companion_app is ready.")

if __name__ == "__main__":
    main()
