# companion_app/companion_app.py
# Module containing classes: DashboardDialog, DummyArgs, functions: check_admin_access, run_headless_migration, run_gui_migration.

# Dual-Mode: Multi-Tab GUI Wizard + Headless CLI Terminal

import sys
import os
import argparse
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
    UI_ASSETS_DIR = getattr(sys, '_MEIPASS', ROOT_DIR)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir in sys.path:
        sys.path.remove(current_dir)
    ROOT_DIR = os.path.abspath(os.path.join(current_dir, '..'))
    UI_ASSETS_DIR = os.path.join(current_dir, "ui_assets")

sys.path.insert(0, ROOT_DIR)

from companion_app.core.controller_saas_migrator import SaasMigratorController
from companion_app.core.controller_create_tenant import CreateTenantController
from companion_app.core.controller_network_config import NetworkConfigController
from companion_app.core.controller_backup import BackupController
from companion_app.core.service_installer import ServiceInstallerController
from companion_app.core.controller_danger_zone import DangerZoneController
from companion_app.core.reset_controller import ResetAdminController
from companion_app.core.headless_reset import run_headless_reset

def check_admin_access() -> bool:
    saas_dir = os.path.join(ROOT_DIR, "synora_saas")
    config_path = os.path.join(saas_dir, "config.ini")
    os.makedirs(saas_dir, exist_ok=True)
    try:
        if os.path.exists(config_path):
            with open(config_path, 'a') as f: pass
        else:
            with open(config_path, 'w') as f: pass
        return True
    except PermissionError:
        return False

# ═══════════════════════════════════════════════════════════════════
#  HEADLESS / CLI MODE
# ═══════════════════════════════════════════════════════════════════

def run_headless_migration(args=None):
    print("======================================================================")
    print(" 🛠️  COMPANION OPERATION / ADMIN DASHBOARD (CLI MODE)")
    print("======================================================================")
    
    if not check_admin_access():
        print("❌ CRITICAL: Access Denied to synora_saas/config.ini.")
        print("Please restart this terminal as Administrator.")
        return 1
        
    if args and getattr(args, 'action', None):
        print(f"Executing automated action: {args.action}")
        if args.action == "backup":
            return BackupController.run_cli_action(getattr(args, 'target_dir', None))
        elif args.action == "migrate":
            from synora_server.logic.migration_bridge import run_interactive_cli_migration
            run_interactive_cli_migration()
            return 0
        elif args.action == "create-user":
            return CreateTenantController.run_cli_action(args)
        elif args.action == "web-config":
            return NetworkConfigController.run_cli_action(getattr(args, 'host', None), getattr(args, 'port', None))
        elif args.action == "danger-zone":
            return DangerZoneController.run_cli_action()
        elif args.action == "reset-admin":
            return run_headless_reset(getattr(args, 'random_password', False), getattr(args, 'custom_password', None))
        else:
            print(f"Unknown action: {args.action}")
            return 1
            
    while True:
        print("\nMain Menu:")
        print("  1. 📦 Database Relocator (Chat DB & SaaS DB)")
        print("  2. 👤 Create SaaS Tenant")
        print("  3. ⚙️ Background Service Installation")
        print("  4. 💾 Backup Local SaaS Database")
        print("  5. 🌐 Network/Web Config")
        print("  6. 🔑 Admin Credentials Recovery")
        print("  7. ⚠️  Danger Zone (Reset Platform)")
        print("  8. Exit")
        choice = input("\nSelect operation (1-8) [8]: ").strip() or "8"
        
        if choice == "8":
            print("\nExiting. Goodbye.")
            return 0
            
        if choice == "1":
            from synora_server.logic.migration_bridge import run_interactive_cli_migration
            run_interactive_cli_migration()
        elif choice == "2":
            CreateTenantController.run_cli_interactive()
        elif choice == "3":
            ServiceInstallerController.run_cli_interactive()
        elif choice == "4":
            BackupController.run_cli_action()
        elif choice == "5":
            NetworkConfigController.run_cli_interactive()
        elif choice == "6":
            run_headless_reset()
        elif choice == "7":
            DangerZoneController.run_cli_action()
        else:
            print("Invalid choice.")

# ═══════════════════════════════════════════════════════════════════
#  GUI MODE
# ═══════════════════════════════════════════════════════════════════

def run_gui_migration():
    from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTabWidget, QMessageBox, QPushButton, QLineEdit, QScrollArea
    from PySide6.QtCore import QSettings, Qt
    from PySide6.QtUiTools import QUiLoader
    
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        print("\n\033[91m[!] CRITICAL: Graphical X11 Display server unavailable or failed to connect.\033[0m")
        print(f"    Error Details: {e}")
        print("\n\033[93m[X11 FORWARDING FAILED]\033[0m")
        print("If you are running this on a remote Ubuntu cloud server via SSH:")
        print("  1. Ensure you connected with X11 Forwarding enabled (e.g. 'ssh -X admin@ip' or 'ssh -Y admin@ip').")
        print("  2. Ensure you have an X-Server running on your local Windows machine (e.g. VcXsrv, Xming).")
        print("  3. Ensure server packages are installed: 'sudo apt install xauth libgl1-mesa-glx libegl1-mesa'")
        print("\n\033[96m[HEADLESS FALLBACK]\033[0m")
        print("To interact with Synora Studio Companion in the terminal without a GUI, run the Headless CLI:")
        print("👉  python companion_app.py --headless\n")
        print("Automatically falling back to Headless Companion Engine mode...\n")
        
        # Fall back to CLI explicitly by re-parsing args and injecting headless mode
        class DummyArgs: pass
        dummy = DummyArgs()
        dummy.action = None
        return run_headless_migration(dummy)
    
    style = """
    * { font-family: "Segoe UI", "Inter", "Roboto", "Helvetica Neue", Arial, sans-serif; font-size: 10pt; }
    QMainWindow, QDialog, QTabWidget::pane { background-color: #f8f9fa; border: none; }
    QTabBar::tab { background-color: #e9ecef; padding: 8px 16px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
    QTabBar::tab:selected { background-color: #ffffff; border-bottom: 2px solid #0078d4; font-weight: bold; }
    QGroupBox { font-weight: bold; border: 1px solid #dee2e6; border-radius: 6px; margin-top: 12px; background-color: #ffffff; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #0078d4; }
    QPushButton { background-color: #0078d4; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #106ebe; }
    QPushButton:pressed { background-color: #005a9e; }
    QPushButton:disabled { background-color: #a0a0a0; }
    QLineEdit, QComboBox { border: 1px solid #ced4da; border-radius: 4px; padding: 6px; background-color: #ffffff; }
    QLineEdit:focus, QComboBox:focus { border: 1px solid #0078d4; }
    QProgressBar { border: 1px solid #ced4da; border-radius: 6px; text-align: center; background-color: #e9ecef; color: #495057; font-weight: bold; }
    QProgressBar::chunk { background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0078d4, stop: 1 #00b4ff); border-radius: 5px; }
    QTextEdit { background-color: #ffffff; border: 1px solid #ced4da; border-radius: 4px; padding: 8px; font-family: "Consolas", "Courier New", monospace; color: #212529; }
    QLabel { color: #212529; }
    """
    app.setStyleSheet(style)
    
    if not check_admin_access():
        QMessageBox.critical(None, "Permission Denied", "Access to synora_saas/config.ini is restricted.\nPlease run as Administrator.")
        return 1

    class DashboardDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Administrator Dashboard")
            self.setMinimumSize(800, 600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
            
            def wrap_in_scroll(widget):
                scroll = QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setWidget(widget)
                scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
                return scroll
            
            loader = QUiLoader()
            dash_path = os.path.join(UI_ASSETS_DIR, "dashboard.ui")
            self.ui = loader.load(dash_path, self)
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0,0,0,0)
            layout.addWidget(self.ui)
            
            self.input_desktop_path = self.ui.findChild(QLineEdit, "input_desktop_path")
            self.btn_browse_desktop = self.ui.findChild(QPushButton, "btn_browse_desktop")
            self.mainTabs = self.ui.findChild(QTabWidget, "mainTabs")
            
            if self.btn_browse_desktop:
                self.btn_browse_desktop.clicked.connect(self._browse_desktop_path)
            
            # Hydrate last path
            self.comp_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Synora_Companion", "Companion_Config")
            last_path = self.comp_settings.value("desktop_config_path", "")
            if self.input_desktop_path and last_path:
                self.input_desktop_path.setText(last_path)
            
            if self.input_desktop_path:
                self.input_desktop_path.textChanged.connect(self._save_desktop_path)
            
            # Load and wire each UI Tab to its isolated controller
            self.saas_tab = loader.load(os.path.join(UI_ASSETS_DIR, "saas_db.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.saas_tab), "📦 Database Relocator")
            self.saas_controller = SaasMigratorController(self.saas_tab)
            # The Backup tool is injected directly into the SaaS Tab UI
            self.backup_controller = BackupController(self.saas_tab)
            btn_backup = self.saas_tab.findChild(QPushButton, "btn_backup")
            if btn_backup: btn_backup.clicked.connect(self.backup_controller.run_gui_backup)
            
            self.tenant_tab = loader.load(os.path.join(UI_ASSETS_DIR, "create_tenant.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.tenant_tab), "👤 Create SaaS Tenant")
            self.tenant_controller = CreateTenantController(self.tenant_tab)
            
            self.service_tab = loader.load(os.path.join(UI_ASSETS_DIR, "service_installer.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.service_tab), "⚙️ Service Setup Wizard")
            self.service_controller = ServiceInstallerController(self.service_tab)
            
            self.web_tab = loader.load(os.path.join(UI_ASSETS_DIR, "web_settings.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.web_tab), "🌐 Network Config")
            self.network_controller = NetworkConfigController(self.web_tab)
            
            self.reset_tab = loader.load(os.path.join(UI_ASSETS_DIR, "reset_admin.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.reset_tab), "🔑 Admin Recovery")
            self.reset_controller = ResetAdminController(self.reset_tab)
            
            self.danger_tab = loader.load(os.path.join(UI_ASSETS_DIR, "danger_zone.ui"), self)
            self.mainTabs.addTab(wrap_in_scroll(self.danger_tab), "⚠️ Danger Zone")
            self.danger_controller = DangerZoneController(self.danger_tab)

        def _browse_desktop_path(self):
            from PySide6.QtWidgets import QFileDialog
            path = QFileDialog.getExistingDirectory(self, "Select Desktop App Storage Root (containing config.ini)")
            if path and self.input_desktop_path:
                self.input_desktop_path.setText(path)
                
        def _save_desktop_path(self, text):
            self.comp_settings.setValue("desktop_config_path", text.strip())

    window = DashboardDialog()
    window.show()
    return app.exec()

def main():
    parser = argparse.ArgumentParser(description="Companion App / Admin Dashboard")
    parser.add_argument("--headless", "--cli", action="store_true", dest="headless", help="Run in headless/CLI mode")
    parser.add_argument("--action", type=str, choices=["migrate", "backup", "create-user", "web-config", "reset-admin", "danger-zone"], help="Automated scriptable action to perform")
    parser.add_argument("--target-dir", type=str, help="Target directory for backup")
    parser.add_argument("--username", type=str, help="Username for create-user action")
    parser.add_argument("--email", type=str, help="Email for create-user action")
    parser.add_argument("--password", type=str, help="Password for create-user action")
    parser.add_argument("--bypass-otp", action="store_true", help="Bypass OTP for create-user action")
    parser.add_argument("--demo-user", action="store_true", help="Inject Demo User")
    parser.add_argument("--delete-demo-user", action="store_true", help="Delete Demo User")
    parser.add_argument("--host", type=str, help="Host binding for web-config")
    parser.add_argument("--port", type=str, help="Port binding for web-config")
    parser.add_argument("--random-password", action="store_true", help="Generate a random password for reset-admin")
    parser.add_argument("--custom-password", type=str, help="Set a custom password for reset-admin")
    parser.add_argument("--desktop-config-path", type=str, help="Path to Desktop App storage root containing config.ini for SSH piggybacking")
    args = parser.parse_args()
    
    if args.desktop_config_path:
        from PySide6.QtCore import QSettings
        comp_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Synora_Companion", "Companion_Config")
        comp_settings.setValue("desktop_config_path", args.desktop_config_path.strip())
        
    if args.headless:
        sys.exit(run_headless_migration(args))
    else:
        sys.exit(run_gui_migration())

if __name__ == "__main__":
    main()
