# companion_app/core/controller_danger_zone.py
# Module containing classes: DangerZoneController, functions: run_cli_action.

from PySide6.QtWidgets import QPushButton, QTextEdit, QMessageBox
from .admin_platform_reset import AdminPlatformReset

class DangerZoneController:
    def __init__(self, ui_tab=None):
        self.ui_tab = ui_tab
        if self.ui_tab:
            self._wire_gui()

    def _wire_gui(self):
        self.btnResetPlatform = self.ui_tab.findChild(QPushButton, "btnResetPlatform")
        self.log_output = self.ui_tab.findChild(QTextEdit, "log_output")
        
        if self.btnResetPlatform:
            self.btnResetPlatform.clicked.connect(self._run_gui_reset)

    def _run_gui_reset(self):
        # Strict warning confirmation
        reply = QMessageBox.question(
            self.ui_tab, 
            "CRITICAL WARNING", 
            "This will permanently delete all non-admin users and their data.\n\nAre you absolutely sure you want to reset the Web Platform?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Double check
            reply2 = QMessageBox.warning(
                self.ui_tab,
                "FINAL CONFIRMATION",
                "You are about to NUKE the platform. This cannot be undone!\n\nType 'YES' mentally, and click Yes to proceed.",
                QMessageBox.Yes | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            
            if reply2 == QMessageBox.Yes:
                self.log_output.append("\n⏳ Initiating Platform Reset...")
                success, msg = AdminPlatformReset.execute_full_reset()
                if success:
                    self.log_output.append("✅ " + msg)
                    QMessageBox.information(self.ui_tab, "Reset Complete", msg)
                else:
                    self.log_output.append("❌ " + msg)
                    QMessageBox.critical(self.ui_tab, "Reset Failed", msg)

    @staticmethod
    def run_cli_action():
        print("\n!!! DANGER ZONE: PLATFORM RESET !!!")
        print("This will permanently delete ALL non-admin users and their data.")
        confirm = input("Type 'RESET' to confirm: ").strip()
        if confirm == 'RESET':
            success, msg = AdminPlatformReset.execute_full_reset()
            print(msg)
            return 0 if success else 1
        else:
            print("Reset cancelled.")
            return 0
