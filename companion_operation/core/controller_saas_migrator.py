# companion_operation/core/controller_saas_migrator.py
# Module containing classes: SaasMigrationWorker, SaasMigratorController, functions: save_config, run, run_cli_interactive.

import os
import sys
from PySide6.QtWidgets import QPushButton, QMessageBox, QComboBox, QTextEdit, QProgressBar, QLabel, QLineEdit
from PySide6.QtCore import QThread, Signal

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def save_config(driver, credentials):
    import configparser
    config_path = os.path.join(ROOT_DIR, "saas", "config.ini")
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    if not config.has_section("TENANT_DB"):
        config.add_section("TENANT_DB")
        
    config.set("TENANT_DB", "driver", driver)
    
    if driver == "postgres":
        config.set("TENANT_DB", "pg_connection_string", credentials.get('pgConnStr', ''))
    elif driver == "mysql":
        config.set("TENANT_DB", "mysql_host", credentials.get('myHost', '127.0.0.1'))
        config.set("TENANT_DB", "mysql_port", credentials.get('myPort', '3306'))
        config.set("TENANT_DB", "mysql_user", credentials.get('myUser', 'root'))
        config.set("TENANT_DB", "mysql_password", credentials.get('myPass', ''))
        config.set("TENANT_DB", "mysql_database", credentials.get('myDB', 'saas_tenants'))
        
    with open(config_path, 'w') as f:
        config.write(f)

class SaasMigrationWorker(QThread):
    log_msg = Signal(str)
    prog_upd = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, driver, credentials):
        super().__init__()
        self.driver = driver
        self.credentials = credentials
        
    def run(self):
        try:
            self.log_msg.emit("Connecting to Source (Turso)...")
            from web.tenant_drivers.turso_tenant_driver import TursoTenantDriver
            source = TursoTenantDriver(db_name="saas_tenants.db")
            
            self.log_msg.emit("Connecting to Target dynamically...")
            if self.driver == "postgres":
                from web.tenant_drivers.postgres_tenant_driver import PostgresTenantDriver
                target = PostgresTenantDriver(self.credentials['pgConnStr'])
            elif self.driver == "mysql":
                from web.tenant_drivers.mysql_tenant_driver import MySQLTenantDriver
                target = MySQLTenantDriver(
                    host=self.credentials['myHost'], port=int(self.credentials['myPort']),
                    user=self.credentials['myUser'], password=self.credentials['myPass'],
                    database=self.credentials['myDB']
                )
            else:
                self.finished.emit(False, "Unsupported target driver.")
                return
                
            from server.logic.migration_bridge import migrate_saas_tenant_database, verify_saas_tenant_integrity
            count = migrate_saas_tenant_database(source, target, progress_callback=lambda m: self.log_msg.emit(m))
            self.prog_upd.emit(70)
            
            self.log_msg.emit("Running Integrity Audit...")
            source_verify = TursoTenantDriver(db_name="saas_tenants.db")
            
            if self.driver == "postgres":
                from web.tenant_drivers.postgres_tenant_driver import PostgresTenantDriver
                target_verify = PostgresTenantDriver(self.credentials['pgConnStr'])
            elif self.driver == "mysql":
                from web.tenant_drivers.mysql_tenant_driver import MySQLTenantDriver
                target_verify = MySQLTenantDriver(
                    host=self.credentials['myHost'], port=int(self.credentials['myPort']),
                    user=self.credentials['myUser'], password=self.credentials['myPass'],
                    database=self.credentials['myDB']
                )
                
            audit = verify_saas_tenant_integrity(source_verify, target_verify, progress_callback=lambda m: self.log_msg.emit(m))
            self.prog_upd.emit(100)
            
            if audit["passed"]:
                save_config(self.driver, self.credentials)
                self.finished.emit(True, f"Relocated {count} accounts safely.\nconfig.ini successfully updated!")
            else:
                self.finished.emit(False, "Integrity audit failed. config.ini was NOT updated to prevent data loss.")
        except Exception as e:
            self.finished.emit(False, str(e))

class SaasMigratorController:
    def __init__(self, ui_tab=None):
        self.ui_tab = ui_tab
        if self.ui_tab:
            self._wire_gui()

    def _wire_gui(self):
        self.saas_btn = self.ui_tab.findChild(QPushButton, "btn_start")
        self.saas_log = self.ui_tab.findChild(QTextEdit, "log_output")
        self.saas_prog = self.ui_tab.findChild(QProgressBar, "progress_bar")
        self.saas_combo = self.ui_tab.findChild(QComboBox, "driverCombo")
        self.sourceInfoLabel = self.ui_tab.findChild(QLabel, "sourceInfoLabel")
        self.lbl_row_2 = self.ui_tab.findChild(QLabel, "label_2")
        
        if self.sourceInfoLabel:
            import configparser
            config_path = os.path.join(ROOT_DIR, "saas", "config.ini")
            driver_display = "Turso / libSQL (Local SQLite)\nsaas_tenants.db"
            if os.path.exists(config_path):
                cp = configparser.ConfigParser()
                cp.read(config_path)
                if "TENANT_DB" in cp and "driver" in cp["TENANT_DB"]:
                    d = cp["TENANT_DB"]["driver"]
                    if d == "postgres":
                        driver_display = "PostgreSQL (psycopg2)"
                        if self.lbl_row_2: self.lbl_row_2.setText(" Host :")
                    elif d == "mysql":
                        driver_display = f"MySQL / MariaDB (pymysql)\n{cp['TENANT_DB'].get('mysql_host', 'localhost')}"
                        if self.lbl_row_2: self.lbl_row_2.setText(" Host :")
            self.sourceInfoLabel.setText(driver_display)
        
        self.myHost = self.ui_tab.findChild(QLineEdit, "myHost")
        self.myPort = self.ui_tab.findChild(QLineEdit, "myPort")
        self.myUser = self.ui_tab.findChild(QLineEdit, "myUser")
        self.myPass = self.ui_tab.findChild(QLineEdit, "myPass")
        self.myDB = self.ui_tab.findChild(QLineEdit, "myDB")
        self.btn_eye = self.ui_tab.findChild(QPushButton, "btn_eye")
        
        from PySide6.QtGui import QIntValidator
        if self.myPort:
            self.myPort.setValidator(QIntValidator(1, 65535, self.ui_tab))
            
        if self.btn_eye and self.myPass:
            def toggle_password(checked):
                if checked:
                    self.myPass.setEchoMode(QLineEdit.Normal)
                else:
                    self.myPass.setEchoMode(QLineEdit.Password)
            self.btn_eye.toggled.connect(toggle_password)
        
        if self.saas_btn:
            self.saas_btn.clicked.connect(self._run_gui)

    def _run_gui(self):
        index = self.saas_combo.currentIndex()
        driver = "postgres" if index == 0 else "mysql"
        
        creds = {}
        creds['myHost'] = self.myHost.text().strip() or "127.0.0.1"
        creds['myPort'] = self.myPort.text().strip() or ("5432" if driver == "postgres" else "3306")
        creds['myUser'] = self.myUser.text().strip() or ("postgres" if driver == "postgres" else "root")
        creds['myPass'] = self.myPass.text().strip()
        creds['myDB'] = self.myDB.text().strip() or "saas_tenants"

        if driver == "postgres":
            creds['pgConnStr'] = f"postgresql://{creds['myUser']}:{creds['myPass']}@{creds['myHost']}:{creds['myPort']}/{creds['myDB']}"

        reply = QMessageBox.question(self.ui_tab, "Confirm", "Start migration to the selected database?\n\nThis will safely rewrite saas/config.ini upon success.", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes: return

        self.saas_btn.setEnabled(False)
        self.saas_log.clear()
        self.worker = SaasMigrationWorker(driver, creds)
        self.worker.log_msg.connect(self.saas_log.append)
        self.worker.prog_upd.connect(self.saas_prog.setValue)
        self.worker.finished.connect(self._saas_done)
        self.worker.start()
        
    def _saas_done(self, success, msg):
        self.saas_btn.setEnabled(True)
        if success:
            QMessageBox.information(self.ui_tab, "Success", msg)
        else:
            QMessageBox.critical(self.ui_tab, "Failed", msg)

    @staticmethod
    def run_cli_interactive():
        print("\n--- SaaS Tenant Upgrader ---")
        print("Source: Local Turso DB (saas_tenants.db)")
        print("\nSelect Target Driver:")
        print("1. PostgreSQL")
        print("2. MySQL / MariaDB")
        driver_choice = input("Choice (1-2) [1]: ").strip() or "1"
        
        credentials = {}
        driver = "postgres" if driver_choice == "1" else "mysql"
        
        credentials['myHost'] = input("Host [127.0.0.1]: ").strip() or "127.0.0.1"
        credentials['myPort'] = input("Port (5432 for PG, 3306 for MySQL): ").strip()
        if not credentials['myPort']:
            credentials['myPort'] = "5432" if driver == "postgres" else "3306"
            
        credentials['myUser'] = input("User: ").strip() or ("postgres" if driver == "postgres" else "root")
        credentials['myPass'] = input("Password: ").strip()
        credentials['myDB'] = input("Database [saas_tenants]: ").strip() or "saas_tenants"
        
        if driver == "postgres":
            credentials['pgConnStr'] = f"postgresql://{credentials['myUser']}:{credentials['myPass']}@{credentials['myHost']}:{credentials['myPort']}/{credentials['myDB']}"

        confirm = input("\nProceed with migration? (y/n) [n]: ").strip().lower()
        if confirm != 'y': return
        
        print("\nRunning pre-flight database connection check...")
        try:
            if driver == "postgres":
                try:
                    import importlib
                    psycopg2 = importlib.import_module("psycopg2")
                    conn = psycopg2.connect(credentials['pgConnStr'], connect_timeout=5)
                    conn.close()
                    print("✅ Pre-flight connection test: Connection successful!")
                except ImportError:
                    print("⚠️  Warning: psycopg2 package not installed. Skipping pre-flight connection check.")
            elif driver == "mysql":
                try:
                    import importlib
                    mysql_connector = importlib.import_module("mysql.connector")
                    conn = mysql_connector.connect(
                        host=credentials['myHost'], port=int(credentials['myPort']),
                        user=credentials['myUser'], password=credentials['myPass'],
                        database=credentials['myDB'],
                        connection_timeout=5
                    )
                    conn.close()
                    print("✅ Pre-flight connection test: Connection successful!")
                except ImportError:
                    print("⚠️  Warning: mysql-connector-python package not installed. Skipping pre-flight connection check.")
        except Exception as check_err:
            print(f"❌ Pre-flight connection test: Connection failed! {check_err}")
            confirm_anyway = input("Do you want to proceed anyway? (y/n) [n]: ").strip().lower()
            if confirm_anyway != 'y':
                print("Migration aborted.")
                return

        try:
            from web.tenant_drivers.turso_tenant_driver import TursoTenantDriver
            source = TursoTenantDriver(db_name="saas_tenants.db")
            
            if driver == "postgres":
                from web.tenant_drivers.postgres_tenant_driver import PostgresTenantDriver
                target = PostgresTenantDriver(credentials['pgConnStr'])
            elif driver == "mysql":
                from web.tenant_drivers.mysql_tenant_driver import MySQLTenantDriver
                target = MySQLTenantDriver(
                    host=credentials['myHost'], port=int(credentials['myPort']),
                    user=credentials['myUser'], password=credentials['myPass'],
                    database=credentials['myDB']
                )
                
            from server.logic.migration_bridge import migrate_saas_tenant_database, verify_saas_tenant_integrity
            
            count = migrate_saas_tenant_database(source, target, progress_callback=lambda log: print(f"  {log}"))
            print(f"✅ Relocated {count} tenants successfully.")
            
            print("Running Integrity Audit...")
            source_verify = TursoTenantDriver(db_name="saas_tenants.db")
            
            if driver == "postgres":
                from web.tenant_drivers.postgres_tenant_driver import PostgresTenantDriver
                target_verify = PostgresTenantDriver(credentials['pgConnStr'])
            elif driver == "mysql":
                from web.tenant_drivers.mysql_tenant_driver import MySQLTenantDriver
                target_verify = MySQLTenantDriver(
                    host=credentials['myHost'], port=int(credentials['myPort']),
                    user=credentials['myUser'], password=credentials['myPass'],
                    database=credentials['myDB']
                )
                
            audit = verify_saas_tenant_integrity(source_verify, target_verify, progress_callback=lambda log: print(f"  {log}"))
            if audit["passed"]:
                save_config(driver, credentials)
                print("✅ Config updated successfully.")
            else:
                print("❌ Integrity audit failed. Config NOT updated.")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
