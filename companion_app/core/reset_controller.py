# admin_reset/reset_controller.py
# Module containing classes: ResetAdminController, functions: on_reset.

import sys
import os

class ResetAdminController:
    def __init__(self, ui_tab):
        from PySide6.QtWidgets import QPushButton, QTextEdit, QRadioButton, QLineEdit
        self.ui_tab = ui_tab

        self.btn_reset = self.ui_tab.findChild(QPushButton, "btn_reset")
        self.btn_close = self.ui_tab.findChild(QPushButton, "btn_close")
        self.log_output = self.ui_tab.findChild(QTextEdit, "log_output")

        self.radio_custom = self.ui_tab.findChild(QRadioButton, "radio_custom")
        self.custom_pass = self.ui_tab.findChild(QLineEdit, "custom_pass")
        if self.radio_custom and self.custom_pass:
            self.radio_custom.toggled.connect(self.custom_pass.setEnabled)

        if self.btn_reset:
            self.btn_reset.clicked.connect(self.on_reset)
        if self.btn_close:
            # We don't want the close button to close the entire companion app if it's just a tab
            self.btn_close.setVisible(False)
        
        if self.log_output:
            self.log_output.append("Waiting for execution command...")

    def _apply_theme(self):
        self.ui_tab.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d1117, stop:0.5 #161b22, stop:1 #0d1117);
                color: #c9d1d9;
            }
            * {
                font-family: "Segoe UI", "Inter", "Roboto", "Helvetica Neue", Arial, sans-serif;
                font-size: 10pt;
            }
            QMainWindow {
                background-color: #0d1117;
            }
            QLabel { color: #c9d1d9; }
            QLabel#subtitle { color: #8b949e; font-style: italic; }
            QTextEdit {
                background-color: #010409;
                color: #58a6ff;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
                font-family: "Consolas", "Courier New", monospace;
            }
            QPushButton {
                background-color: #238636;
                color: white;
                border: 1px solid rgba(240, 246, 252, 0.1);
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2ea043; }
            QPushButton:pressed { background-color: #238636; }
            QPushButton:disabled { background-color: #21262d; color: #484f58; border: 1px solid #30363d; }
            QLineEdit {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px;
                color: #c9d1d9;
            }
            QLineEdit:focus { border: 1px solid #58a6ff; }
            QProgressBar {
                border: 1px solid #30363d;
                border-radius: 6px;
                text-align: center;
                background-color: #010409;
                color: #c9d1d9;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #238636, stop: 1 #2ea043);
                border-radius: 5px;
            }
            QPushButton#btn_reset {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d73a49, stop:1 #cb2431);
                color: #ffffff;
                border: 1px solid #cb2431;
                border-radius: 8px;
            }
            QPushButton#btn_reset:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #cb2431, stop:1 #b31d28);
            }
            QPushButton#btn_close {
                background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 8px;
            }
            QPushButton#btn_close:hover { background-color: #30363d; border: 1px solid #484f58; }
        """)

    def on_reset(self):
        from PySide6.QtWidgets import QRadioButton, QLineEdit, QMessageBox
        from synora_server.logic.tenant.tenant_db import TenantDatabaseManager
        import string
        import random

        radio_default = self.ui_tab.findChild(QRadioButton, "radio_default")
        radio_random = self.ui_tab.findChild(QRadioButton, "radio_random")
        radio_custom = self.ui_tab.findChild(QRadioButton, "radio_custom")
        line_edit = self.ui_tab.findChild(QLineEdit, "custom_pass")

        if radio_random and radio_random.isChecked():
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        elif radio_custom and radio_custom.isChecked():
            new_password = line_edit.text()
            if not new_password:
                QMessageBox.critical(self.ui_tab, "Error", "Custom password cannot be empty.")
                return
        else:
            new_password = "admin"

        reply = QMessageBox.question(self.ui_tab, "Confirm Global Reset", "Are you sure you want to reset the Master Admin Credentials?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log_output.append("\n▶ Initiating universal master reset sequence...")
            try:
                db = TenantDatabaseManager()
                db.reset_admin_account(new_password)
                self.log_output.append("✅ Successfully synchronized Master Credentials!")
                self.log_output.append(f"  Username: admin\n  Password: {new_password}\n  API Key: admin_master_passport")
                QMessageBox.information(self.ui_tab, "Success", "Master admin account reset to specified password.")
            except Exception as e:
                self.log_output.append(f"❌ Failed: {str(e)}")
                QMessageBox.critical(self.ui_tab, "Error", f"Reset failed:\n{e}")
