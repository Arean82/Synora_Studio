# companion_app/core/controller_backup.py
# Module containing classes: BackupController, functions: run_gui_backup, run_cli_action.

import os
import datetime
import shutil
import subprocess
import configparser
from PySide6.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QApplication

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class BackupController:
    def __init__(self, ui_parent=None):
        self.ui_parent = ui_parent

    def run_gui_backup(self):
        config_path = os.path.join(ROOT_DIR, "synora_saas", "config.ini")
        driver = "sqlite"
        cp = configparser.ConfigParser()
        if os.path.exists(config_path):
            cp.read(config_path)
            if "TENANT_DB" in cp and "driver" in cp["TENANT_DB"]:
                driver = cp["TENANT_DB"]["driver"]
                
        if driver == "sqlite" or driver == "turso":
            db_path = os.path.join(ROOT_DIR, "synora_server", "data", "saas_tenants.db")
            if not os.path.exists(db_path):
                QMessageBox.critical(self.ui_parent, "Error", "Local Turso DB not found.")
                return
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            target_file, _ = QFileDialog.getSaveFileName(self.ui_parent, "Save Local Backup", f"saas_tenants_backup_{stamp}.db", "SQLite Database (*.db);;All Files (*)")
            if not target_file: return
            try:
                shutil.copy2(db_path, target_file)
                QMessageBox.information(self.ui_parent, "Backup Success", f"Database backed up to:\n{target_file}")
            except Exception as e:
                QMessageBox.critical(self.ui_parent, "Backup Failed", str(e))
        else:
            db_user = cp['TENANT_DB'].get('user', 'root')
            db_host = cp['TENANT_DB'].get('host', '127.0.0.1')
            db_port = cp['TENANT_DB'].get('port', '5432' if driver == 'postgres' else '3306')
            db_name = cp['TENANT_DB'].get('database', 'saas_tenants')
            pwd = cp['TENANT_DB'].get('password', '')
            
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if driver == "postgres":
                formats = ["Plain Text (.sql)", "Custom Compressed (.dump) (Recommended)"]
                format_choice, ok_fmt = QInputDialog.getItem(self.ui_parent, "PostgreSQL Dump Format", 
                                                            "Select backup format:\n(Compressed is recommended for use with pg_restore)", 
                                                            formats, 1, False)
                if not ok_fmt: return
                
                if "Compressed" in format_choice:
                    target_file, _ = QFileDialog.getSaveFileName(self.ui_parent, "Save PostgreSQL Dump", f"backup_postgres_{stamp}.dump", "PostgreSQL Custom Dump (*.dump);;All Files (*)")
                    if not target_file: return
                    cmd = ["pg_dump", "-h", db_host, "-p", str(db_port), "-U", db_user, "-F", "c", "-f", target_file, db_name]
                else:
                    target_file, _ = QFileDialog.getSaveFileName(self.ui_parent, "Save PostgreSQL Dump", f"backup_postgres_{stamp}.sql", "SQL Dump (*.sql);;All Files (*)")
                    if not target_file: return
                    cmd = ["pg_dump", "-h", db_host, "-p", str(db_port), "-U", db_user, "-F", "p", "-f", target_file, db_name]
                    
                env = os.environ.copy()
                env["PGPASSWORD"] = pwd
            else:
                target_file, _ = QFileDialog.getSaveFileName(self.ui_parent, "Save MySQL Dump", f"backup_mysql_{stamp}.sql", "SQL Dump (*.sql);;All Files (*)")
                if not target_file: return
                cmd = ["mysqldump", "-h", db_host, "-P", str(db_port), "-u", db_user, f"-p{pwd}", "--result-file", target_file, db_name]
                env = os.environ.copy()
            
            try:
                from PySide6.QtCore import Qt
                QApplication.setOverrideCursor(Qt.WaitCursor)
                res = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
                QApplication.restoreOverrideCursor()
                QMessageBox.information(self.ui_parent, "Backup Success", f"Native SQL Dump generated successfully at:\n{target_file}")
            except subprocess.CalledProcessError as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self.ui_parent, "Backup Failed", f"Database dump failed:\n{e.stderr}")
            except FileNotFoundError:
                QApplication.restoreOverrideCursor()
                tool = "pg_dump" if driver == "postgres" else "mysqldump"
                QMessageBox.critical(self.ui_parent, "Tool Not Found", f"The command-line tool '{tool}' is not installed or not available in the system PATH.\n\nPlease install the native database utilities to perform live backups.")
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self.ui_parent, "Error", f"An unexpected error occurred:\n{str(e)}")

    @staticmethod
    def run_cli_action(target_dir=None):
        db_path = os.path.join(ROOT_DIR, "synora_server", "data", "saas_tenants.db")
        if not os.path.exists(db_path):
            print("❌ Local Turso Database not found at:", db_path)
            return 1
        
        dest = target_dir
        if not dest:
            dest = input("Enter backup destination folder path: ").strip()
            
        if not dest or not os.path.exists(dest):
            print("Invalid directory.")
            return 1
            
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = os.path.join(dest, f"saas_tenants_backup_{stamp}.db")
        try:
            shutil.copy2(db_path, target_file)
            print(f"✅ Database backed up to: {target_file}")
            return 0
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return 1
