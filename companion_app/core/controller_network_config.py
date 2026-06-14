# companion_app/core/controller_network_config.py
# Module containing classes: NetworkConfigController, functions: run_cli_interactive, run_cli_action.

import os
from PySide6.QtWidgets import QLineEdit, QPushButton, QMessageBox
from synora_server.logic.tenant.config_manager import SaaSConfigManager

class NetworkConfigController:
    def __init__(self, ui_tab=None):
        self.ui_tab = ui_tab
        if self.ui_tab:
            self._wire_gui()

    def _wire_gui(self):
        self.web_config = SaaSConfigManager()
        
        self.hostEdit = self.ui_tab.findChild(QLineEdit, "hostEdit")
        self.portEdit = self.ui_tab.findChild(QLineEdit, "portEdit")
        self.btn_save = self.ui_tab.findChild(QPushButton, "btn_save")
        
        if self.hostEdit:
            self.hostEdit.setText(self.web_config.get_str("NETWORK", "host", "127.0.0.1"))
        if self.portEdit:
            self.portEdit.setText(self.web_config.get_str("NETWORK", "port", "8080"))
            
        from PySide6.QtGui import QIntValidator
        if self.portEdit:
            self.portEdit.setValidator(QIntValidator(1, 65535, self.ui_tab))
            
        if self.btn_save:
            self.btn_save.clicked.connect(self._save_gui_settings)

    def _save_gui_settings(self):
        if not self.hostEdit or not self.portEdit: return
        h = self.hostEdit.text().strip()
        p = self.portEdit.text().strip()
        
        if not h or not p:
            QMessageBox.warning(self.ui_tab, "Validation Error", "Host and Port cannot be empty.")
            return
            
        self.web_config.set_val("NETWORK", "host", h)
        self.web_config.set_val("NETWORK", "port", p)
        self.web_config.set_local_url(h, int(p))
        self.web_config.save()
        
        QMessageBox.information(self.ui_tab, "Saved", f"Network settings successfully applied.\n\nListening on: http://{h}:{p}\n\nPlease restart the Web Portal service.")

    @staticmethod
    def run_cli_interactive():
        config = SaaSConfigManager()
        print("\n--- Network/Web Config ---")
        current_host = config.get_str("NETWORK", "host", "127.0.0.1")
        current_port = config.get_str("NETWORK", "port", "8080")
        
        print(f"Current Host: {current_host}")
        print(f"Current Port: {current_port}")
        
        new_host = input(f"Enter new host address [{current_host}]: ").strip() or current_host
        new_port_str = input(f"Enter new listening port [{current_port}]: ").strip() or current_port
        
        try:
            new_port = int(new_port_str)
            if not (1 <= new_port <= 65535):
                raise ValueError()
        except ValueError:
            print("❌ Error: Invalid port. Must be an integer between 1 and 65535.")
            return
            
        config.set_val("NETWORK", "host", new_host)
        config.set_val("NETWORK", "port", str(new_port))
        config.set_local_url(new_host, new_port)
        config.save()
        print("✅ Network configuration updated successfully.")
        print("ℹ️  Note: You must restart the Web Portal service to apply changes.")

    @staticmethod
    def run_cli_action(host, port_str):
        if not host or not port_str:
            print("❌ Error: --host and --port are required for 'web-config' action.")
            return 1
        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                raise ValueError()
        except ValueError:
            print("❌ Error: Invalid port value.")
            return 1
            
        config = SaaSConfigManager()
        config.set_val("NETWORK", "host", host)
        config.set_val("NETWORK", "port", str(port))
        config.set_local_url(host, port)
        config.save()
        print(f"✅ Network configuration successfully updated to http://{host}:{port}")
        return 0
