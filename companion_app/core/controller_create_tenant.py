# companion_app/core/controller_create_tenant.py
# Module containing classes: CreateTenantController, functions: run_cli_action, run_cli_interactive, execute_creation.

import json
import pyotp
import secrets
from PySide6.QtWidgets import QLineEdit, QCheckBox, QPushButton, QTextEdit, QMessageBox
from synora_server.logic.tenant.tenant_db import TenantDatabaseManager
from .admin_demo_manager import AdminDemoManager

class CreateTenantController:
    def __init__(self, ui_tab=None):
        self.ui_tab = ui_tab
        if self.ui_tab:
            self._wire_gui()

    def _wire_gui(self):
        self.tenantUser = self.ui_tab.findChild(QLineEdit, "tenantUser")
        self.tenantEmail = self.ui_tab.findChild(QLineEdit, "tenantEmail")
        self.tenantPass = self.ui_tab.findChild(QLineEdit, "tenantPass")
        self.checkBypassOTP = self.ui_tab.findChild(QCheckBox, "checkBypassOTP")
        self.btn_create_tenant = self.ui_tab.findChild(QPushButton, "btn_create")
        self.tenant_log = self.ui_tab.findChild(QTextEdit, "log_output")
        
        self.checkEnableDemo = self.ui_tab.findChild(QCheckBox, "checkEnableDemo")
        self.btnDeleteDemo = self.ui_tab.findChild(QPushButton, "btnDeleteDemo")
        
        if self.btn_create_tenant:
            self.btn_create_tenant.clicked.connect(self._run_gui_tenant)
            
        if self.checkEnableDemo and self.btnDeleteDemo:
            self.checkEnableDemo.stateChanged.connect(self._toggle_demo_user)
            self.btnDeleteDemo.clicked.connect(self._delete_demo_user)
            self._update_demo_ui_state()

    def _update_demo_ui_state(self):
        is_enabled = AdminDemoManager.is_demo_enabled()
        self.checkEnableDemo.blockSignals(True)
        self.checkEnableDemo.setChecked(is_enabled)
        self.checkEnableDemo.setEnabled(not is_enabled)
        self.checkEnableDemo.blockSignals(False)
        self.btnDeleteDemo.setVisible(is_enabled)
        
    def _toggle_demo_user(self, state):
        if state:
            success, msg = AdminDemoManager.inject_demo_user()
            if success:
                self.tenant_log.append("\n✅ " + msg)
                QMessageBox.information(self.ui_tab, "Demo User", msg)
            else:
                self.tenant_log.append("\n❌ Demo User Failed: " + msg)
                QMessageBox.critical(self.ui_tab, "Demo User Error", msg)
            self._update_demo_ui_state()
            
    def _delete_demo_user(self):
        success, msg = AdminDemoManager.remove_demo_user()
        if success:
            self.tenant_log.append("\n🗑️ " + msg)
        else:
            self.tenant_log.append("\n❌ Delete Demo User Failed: " + msg)
            QMessageBox.critical(self.ui_tab, "Demo User Error", msg)
        self._update_demo_ui_state()

    def _run_gui_tenant(self):
        if not self.tenantUser or not self.tenantEmail or not self.tenantPass: return
        user = self.tenantUser.text().strip()
        email = self.tenantEmail.text().strip()
        pwd = self.tenantPass.text().strip()
        bypass = self.checkBypassOTP.isChecked() if self.checkBypassOTP else True
        
        if not user or not email or not pwd:
            QMessageBox.warning(self.ui_tab, "Error", "All fields are required.")
            return
            
        try:
            db = TenantDatabaseManager()
            api_key = f"sk-{secrets.token_urlsafe(24)}"
            
            user_id, err, otp_secret = db.register_user(api_key, user, email, pwd)
            if err:
                self.tenant_log.append(f"❌ Failed: {err}")
                return
                
            if bypass:
                with db.get_connection() as conn:
                    conn.execute("UPDATE users SET settings_blob = ? WHERE id = ?", (json.dumps({"otp_verified": True}), user_id))
                    conn.commit()
                    
            totp = pyotp.TOTP(otp_secret)
            current_code = totp.now()
            
            self.tenant_log.append("\n✅ Tenant Provisioned Successfully!")
            self.tenant_log.append(f"Username : {user}")
            self.tenant_log.append(f"Email    : {email}")
            self.tenant_log.append(f"Password : {pwd}")
            self.tenant_log.append(f"API Key  : {api_key}")
            self.tenant_log.append(f"Bypassed : {'Yes' if bypass else 'No'}")
            if not bypass:
                self.tenant_log.append(f"OTP Secrt: {otp_secret}")
                self.tenant_log.append(f"Live Code: {current_code} (Valid for 30s)")
        except Exception as e:
            self.tenant_log.append(f"❌ Error: {str(e)}")

    @staticmethod
    def run_cli_action(args):
        if getattr(args, 'demo_user', False):
            success, msg = AdminDemoManager.inject_demo_user()
            print(msg)
            return 0 if success else 1
        if getattr(args, 'delete_demo_user', False):
            success, msg = AdminDemoManager.remove_demo_user()
            print(msg)
            return 0 if success else 1
            
        user = getattr(args, 'username', None) or "demo_user"
        email = getattr(args, 'email', None) or "example@example.com"
        pwd = getattr(args, 'password', None) or "password123"
        bypass = getattr(args, 'bypass_otp', False)
        return CreateTenantController.execute_creation(user, email, pwd, bypass)

    @staticmethod
    def run_cli_interactive():
        print("\n--- Create SaaS Tenant ---")
        user = input("Username [demo_user]: ").strip() or "demo_user"
        email = input("Email [example@example.com]: ").strip() or "example@example.com"
        pwd = input("Password [password123]: ").strip() or "password123"
        bypass = input("Bypass OTP (Auto-Verify)? (y/n) [y]: ").strip().lower() != 'n'
        CreateTenantController.execute_creation(user, email, pwd, bypass)

    @staticmethod
    def execute_creation(username, email, password, bypass_otp):
        try:
            db = TenantDatabaseManager()
            api_key = f"sk-{secrets.token_urlsafe(24)}"
            
            user_id, err, otp_secret = db.register_user(api_key, username, email, password)
            if err:
                print(f"❌ Failed: {err}")
                return 1
                
            if bypass_otp:
                with db.get_connection() as conn:
                    conn.execute("UPDATE users SET settings_blob = ? WHERE id = ?", (json.dumps({"otp_verified": True}), user_id))
                    conn.commit()
                    
            totp = pyotp.TOTP(otp_secret)
            current_code = totp.now()
            
            print(f"\n✅ Tenant Provisioned Successfully!")
            print(f"Username : {username}")
            print(f"Email    : {email}")
            print(f"Password : {password}")
            print(f"API Key  : {api_key}")
            print(f"Bypassed : {'Yes' if bypass_otp else 'No'}")
            if not bypass_otp:
                print(f"OTP Secrt: {otp_secret}")
                print(f"Live Code: {current_code}")
                
            return 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
