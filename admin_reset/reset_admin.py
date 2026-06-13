# admin_reset/reset_admin.py
# Module containing functions: run_gui_reset, main.

# Designed to run securely as a standalone binary (reset_admin.exe) and compatible with system services.

import sys
import os

# Absolute service-friendly pathing resolution
if getattr(sys, 'frozen', False):
    root_dir = os.path.dirname(sys.executable)
else:
    # operator_tools/admin_reset/reset_admin.py is located under project_root/operator_tools/admin_reset/
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, root_dir)

from web.core.tenant_db import TenantDatabaseManager
import argparse
from core.headless_reset import run_headless_reset

# ═══════════════════════════════════════════════════════════════════
#  GUI MODE — PySide6 XML Loader
# ═══════════════════════════════════════════════════════════════════
def run_gui_reset():
    from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import QIcon

    from admin_reset.reset_controller import ResetAdminController

    app = QApplication(sys.argv)
    app.setApplicationName("Reset Admin")
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    icon_path = os.path.join(base_path, "resources_rest", "app_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    controller = ResetAdminController()
    controller.dialog.show()
    return app.exec()

# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Universal Master Password Reset Sequence")
    parser.add_argument("--headless", "--cli", action="store_true", help="Run in CLI mode without GUI.")
    parser.add_argument("--random-password", action="store_true", help="Generate a random password.")
    parser.add_argument("--custom-password", type=str, help="Set a custom password.")
    args = parser.parse_args()

    if args.headless:
        sys.exit(run_headless_reset(random_pass=args.random_password, custom_pass=args.custom_password))
    else:
        sys.exit(run_gui_reset())

if __name__ == "__main__":
    main()
