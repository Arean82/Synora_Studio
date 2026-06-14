# desktop/ui/gen_settings_dialog.py
# Module containing classes: GenSettingsDialog, functions: setup_api_credentials_ui, update_api_buttons_ui, on_toggle_api.

import os
import uuid
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDoubleSpinBox, QSpinBox, QComboBox, QLabel, QPushButton, QCheckBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSettings, Qt
from PySide6.QtGui import QIcon

from synora_server.utils.path_utils import get_resource_path, get_app_settings
from desktop.ui.shared_widgets import set_app_icon

class GenSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Generation Parameters")
        self.setMinimumWidth(480)
        
        # Ensure appropriate taskbar handling for user convenience
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        set_app_icon(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal) # Freeze main window until this closes
        self.showNormal() # Crucial safety check to ensure visual surfacing
        
        # --- APPLY VISUAL THEME STYLES ---
        settings = get_app_settings()
        is_dark = settings.value("theme", "light") == "dark"
        if is_dark:
            self.setStyleSheet("""
                QDialog { background-color: #252526; color: #ffffff; }
                QLabel { color: #ffffff; }
                QDoubleSpinBox, QSpinBox, QComboBox { 
                    background-color: #2d2d2d; 
                    color: #ffffff; 
                    border: 1px solid #3c3c3c; 
                    border-radius: 5px; 
                    padding: 5px; 
                }
                QDoubleSpinBox:disabled, QSpinBox:disabled {
                    background-color: #1e1e1e; 
                    color: #777777; 
                    border: 1px solid #252526;
                }
                QAbstractItemView {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    selection-background-color: #0078d4;
                }
                QTabWidget::pane {
                    border: 1px solid #3c3c3c;
                    border-radius: 6px;
                    background-color: #1e1e1e;
                    padding: 10px;
                }
                QTabBar::tab {
                    background: #2d2d2d;
                    color: #aaaaaa;
                    padding: 8px 16px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    margin-right: 2px;
                    border: 1px solid #3c3c3c;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #1e1e1e;
                    color: #ffffff;
                    font-weight: bold;
                    border-bottom: 2px solid #0078d4;
                }
                QTabBar::tab:hover {
                    background: #252526;
                    color: #ffffff;
                }
                QPushButton#cancel_btn { 
                    background-color: #3c3c3c; 
                    color: white; 
                    border: none; 
                    padding: 6px; 
                    border-radius: 4px; 
                }
                QPushButton#cancel_btn:hover { background-color: #4c4c4c; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background-color: #ffffff; color: #333333; }
                QDoubleSpinBox, QSpinBox, QComboBox { 
                    background-color: #f5f5f5; 
                    border: 1px solid #cccccc; 
                    border-radius: 5px; 
                    padding: 5px; 
                }
                QTabWidget::pane {
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    background-color: #fafafa;
                    padding: 10px;
                }
                QTabBar::tab {
                    background: #e1e1e1;
                    color: #666666;
                    padding: 8px 16px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    margin-right: 2px;
                    border: 1px solid #cccccc;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #fafafa;
                    color: #0078d4;
                    font-weight: bold;
                    border-bottom: 2px solid #0078d4;
                }
                QTabBar::tab:hover {
                    background: #f0f0f0;
                    color: #333333;
                }
                QPushButton#cancel_btn { 
                    background-color: #e1e1e1; 
                    border: 1px solid #cccccc; 
                    padding: 6px; 
                    border-radius: 4px; 
                }
            """)
        
        # Load from XML UI using the established, reliable loading pattern
        loader = QUiLoader()
        ui_file_path = get_resource_path("ui_designer/gen_settings.ui")
        
        # Load the UI container passing self as parent to attach properly
        self.ui = loader.load(str(ui_file_path), self)
        
        if self.ui and self.ui.layout():
            self.setLayout(self.ui.layout())
            
        self.setMinimumSize(500, 480)
        self.resize(500, 480)
        
        # Bind references
        self.preset_combo = self.findChild(QComboBox, "preset_combo")
        self.temp_input = self.findChild(QDoubleSpinBox, "temp_input")
        self.tokens_input = self.findChild(QSpinBox, "tokens_input")
        self.temp_desc = self.findChild(QLabel, "temp_desc")
        self.token_desc = self.findChild(QLabel, "token_desc")
        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")
        
        # Logging Bindings
        self.log_enable_cb = self.findChild(QCheckBox, "log_enable_cb")
        self.debug_enable_cb = self.findChild(QCheckBox, "debug_enable_cb")
        
        # Signal bindings
        if self.temp_input:
            self.temp_input.valueChanged.connect(self.update_temp_explanation)
        if self.tokens_input:
            self.tokens_input.valueChanged.connect(self.update_tokens_explanation)
        if self.preset_combo:
            self.preset_combo.currentIndexChanged.connect(self.on_preset_changed)
        if self.save_btn:
            self.save_btn.clicked.connect(self.save_and_close)
        if self.cancel_btn:
            self.cancel_btn.clicked.connect(self.reject)
        
        self.setup_rerank_ui(is_dark)
        self.setup_api_credentials_ui()
        self.setup_redis_ui(is_dark)
        self.setup_ssh_ui(is_dark)
        self.load_current_settings()
        
    def setup_ssh_ui(self, is_dark: bool):
        from PySide6.QtWidgets import QGroupBox, QCheckBox, QLineEdit, QSpinBox, QPushButton, QFileDialog
        
        self.ssh_group = self.findChild(QGroupBox, "ssh_group")
        self.ssh_enable_cb = self.findChild(QCheckBox, "ssh_enable_cb")
        self.ssh_host_input = self.findChild(QLineEdit, "ssh_host_input")
        self.ssh_port_input = self.findChild(QSpinBox, "ssh_port_input")
        self.ssh_user_input = self.findChild(QLineEdit, "ssh_user_input")
        self.ssh_pass_input = self.findChild(QLineEdit, "ssh_pass_input")
        self.ssh_key_input = self.findChild(QLineEdit, "ssh_key_input")
        self.ssh_key_pass_input = self.findChild(QLineEdit, "ssh_key_pass_input")
        self.btn_browse_key = self.findChild(QPushButton, "btn_browse_key")
        
        if not self.ssh_enable_cb:
            return
            
        if is_dark:
            if self.ssh_group:
                self.ssh_group.setStyleSheet("""
                    QGroupBox { font-weight: bold; color: #ffffff; border: 1px solid #3c3c3c; border-radius: 6px; margin-top: 15px; padding-top: 20px; }
                    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 10px; padding: 0 5px; }
                    QCheckBox { color: #ffffff; font-weight: normal; }
                    QLineEdit, QSpinBox { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3c3c3c; border-radius: 5px; padding: 5px; }
                    QLineEdit:disabled, QSpinBox:disabled { background-color: #1e1e1e; color: #777777; border: 1px solid #252526; }
                    QPushButton { background-color: #3c3c3c; color: white; border: none; padding: 6px; border-radius: 4px; }
                    QPushButton:hover { background-color: #4c4c4c; }
                """)
        else:
            if self.ssh_group:
                self.ssh_group.setStyleSheet("""
                    QGroupBox { font-weight: bold; color: #333333; border: 1px solid #cccccc; border-radius: 6px; margin-top: 15px; padding-top: 20px; }
                    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 10px; padding: 0 5px; }
                    QCheckBox { color: #333333; font-weight: normal; }
                    QLineEdit, QSpinBox { background-color: #f5f5f5; border: 1px solid #cccccc; border-radius: 5px; padding: 5px; }
                    QLineEdit:disabled, QSpinBox:disabled { background-color: #e1e1e1; color: #aaaaaa; border: 1px solid #cccccc; }
                    QPushButton { background-color: #e1e1e1; border: 1px solid #cccccc; padding: 6px; border-radius: 4px; }
                """)
                
        self.ssh_enable_cb.toggled.connect(self.on_ssh_enabled_toggled)
        self.btn_browse_key.clicked.connect(self.on_browse_ssh_key)
        
    def on_ssh_enabled_toggled(self, checked: bool):
        if hasattr(self, "ssh_host_input"): self.ssh_host_input.setEnabled(checked)
        if hasattr(self, "ssh_port_input"): self.ssh_port_input.setEnabled(checked)
        if hasattr(self, "ssh_user_input"): self.ssh_user_input.setEnabled(checked)
        if hasattr(self, "ssh_pass_input") and self.ssh_pass_input: self.ssh_pass_input.setEnabled(checked)
        if hasattr(self, "ssh_key_input"): self.ssh_key_input.setEnabled(checked)
        if hasattr(self, "ssh_key_pass_input") and self.ssh_key_pass_input: self.ssh_key_pass_input.setEnabled(checked)
        if hasattr(self, "btn_browse_key"): self.btn_browse_key.setEnabled(checked)
        
    def on_browse_ssh_key(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Select SSH Private Key", "", "Key Files (*.pem *.ppk);;All Files (*)")
        if path:
            self.ssh_key_input.setText(path)
        
    def setup_api_credentials_ui(self):
        from PySide6.QtWidgets import QLineEdit
        self.saas_host_input = self.findChild(QLineEdit, "saas_host_input")
        self.saas_token_input = self.findChild(QLineEdit, "saas_token_input")
        
        if not (self.saas_host_input and self.saas_token_input):
            return
            
        settings = get_app_settings()
        
        # Load state
        host = settings.value("saas_host_url", "")
        token = settings.value("saas_access_token", "")
            
        self.saas_host_input.setText(str(host))
        self.saas_token_input.setText(str(token))

    def setup_rerank_ui(self, is_dark: bool):
        """Resolves references to Advanced Retrieval Reranking elements loaded from the UI file, and applies dynamic styling."""
        from PySide6.QtWidgets import QGroupBox, QCheckBox, QComboBox, QLineEdit
        
        self.rerank_group = self.findChild(QGroupBox, "rerank_group")
        self.rerank_enable_cb = self.findChild(QCheckBox, "rerank_enable_cb")
        self.rerank_engine_combo = self.findChild(QComboBox, "rerank_engine_combo")
        self.rerank_endpoint_input = self.findChild(QLineEdit, "rerank_endpoint_input")
        self.rerank_key_input = self.findChild(QLineEdit, "rerank_key_input")
        
        # Premium CSS styling matching the active dialog theme
        if is_dark:
            if self.rerank_group:
                self.rerank_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #ffffff;
                        border: 1px solid #3c3c3c;
                        border-radius: 6px;
                        margin-top: 15px;
                        padding-top: 20px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 5px;
                    }
                    QCheckBox { color: #ffffff; font-weight: normal; }
                    QLineEdit, QComboBox {
                        background-color: #2d2d2d; 
                        color: #ffffff; 
                        border: 1px solid #3c3c3c; 
                        border-radius: 5px; 
                        padding: 5px; 
                    }
                    QLineEdit:disabled, QComboBox:disabled {
                        background-color: #1e1e1e;
                        color: #777777;
                        border: 1px solid #252526;
                    }
                """)
        else:
            if self.rerank_group:
                self.rerank_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #333333;
                        border: 1px solid #cccccc;
                        border-radius: 6px;
                        margin-top: 15px;
                        padding-top: 20px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 5px;
                    }
                    QCheckBox { color: #333333; font-weight: normal; }
                    QLineEdit, QComboBox {
                        background-color: #f5f5f5; 
                        border: 1px solid #cccccc; 
                        border-radius: 5px; 
                        padding: 5px; 
                    }
                    QLineEdit:disabled, QComboBox:disabled {
                        background-color: #e1e1e1;
                        color: #aaaaaa;
                        border: 1px solid #cccccc;
                    }
                """)
            
        # Scale dialog size to host the new GroupBox without clipping
        self.setMinimumSize(500, 480)
        self.resize(500, 480)
        
        # Connect visual signal reactions
        if self.rerank_enable_cb:
            self.rerank_enable_cb.toggled.connect(self.on_rerank_enabled_toggled)
        if self.rerank_engine_combo:
            self.rerank_engine_combo.currentIndexChanged.connect(self.on_rerank_engine_changed)

    def on_rerank_enabled_toggled(self, checked: bool):
        """Disables or enables reranker input fields dynamically depending on toggle state."""
        self.rerank_engine_combo.setEnabled(checked)
        if checked:
            self.on_rerank_engine_changed(self.rerank_engine_combo.currentIndex())
        else:
            self.rerank_endpoint_input.setEnabled(False)
            self.rerank_key_input.setEnabled(False)

    def on_rerank_engine_changed(self, index: int):
        """Shows/hides custom endpoint and secret key parameters depending on selected model style."""
        if not self.rerank_enable_cb.isChecked():
            return
            
        if index == 0:  # Local Mode
            self.rerank_endpoint_input.setEnabled(False)
            self.rerank_key_input.setEnabled(False)
        elif index == 1:  # Cloud Cohere Mode
            self.rerank_endpoint_input.setEnabled(False)
            self.rerank_key_input.setEnabled(True)
        elif index == 2:  # Custom OpenAPI Mode
            self.rerank_endpoint_input.setEnabled(True)
            self.rerank_key_input.setEnabled(True)
        
    def setup_redis_ui(self, is_dark: bool):
        """Resolves references to Redis Configuration widgets loaded from the UI file, and applies dynamic styling."""
        from PySide6.QtWidgets import QGroupBox, QCheckBox, QLineEdit, QSpinBox
        
        self.redis_group = self.findChild(QGroupBox, "redis_group")
        self.redis_enable_cb = self.findChild(QCheckBox, "redis_enable_cb")
        self.redis_host_input = self.findChild(QLineEdit, "redis_host_input")
        self.redis_port_input = self.findChild(QSpinBox, "redis_port_input")
        self.redis_password_input = self.findChild(QLineEdit, "redis_password_input")
        
        if not (self.redis_enable_cb and self.redis_host_input and self.redis_port_input and self.redis_password_input):
            return
            
        # Premium CSS styling matching the active dialog theme
        if is_dark:
            if self.redis_group:
                self.redis_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #ffffff;
                        border: 1px solid #3c3c3c;
                        border-radius: 6px;
                        margin-top: 15px;
                        padding-top: 20px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 5px;
                    }
                    QCheckBox { color: #ffffff; font-weight: normal; }
                    QLineEdit, QSpinBox {
                        background-color: #2d2d2d; 
                        color: #ffffff; 
                        border: 1px solid #3c3c3c; 
                        border-radius: 5px; 
                        padding: 5px; 
                    }
                    QLineEdit:disabled, QSpinBox:disabled {
                        background-color: #1e1e1e;
                        color: #777777;
                        border: 1px solid #252526;
                    }
                """)
        else:
            if self.redis_group:
                self.redis_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        color: #333333;
                        border: 1px solid #cccccc;
                        border-radius: 6px;
                        margin-top: 15px;
                        padding-top: 20px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 5px;
                    }
                    QCheckBox { color: #333333; font-weight: normal; }
                    QLineEdit, QSpinBox {
                        background-color: #f5f5f5; 
                        border: 1px solid #cccccc; 
                        border-radius: 5px; 
                        padding: 5px; 
                    }
                    QLineEdit:disabled, QSpinBox:disabled {
                        background-color: #e1e1e1;
                        color: #aaaaaa;
                        border: 1px solid #cccccc;
                    }
                """)
                
        # Connect signals
        self.redis_enable_cb.toggled.connect(self.on_redis_enabled_toggled)

    def on_redis_enabled_toggled(self, checked: bool):
        """Toggles enable states of Redis input widgets."""
        if hasattr(self, "redis_host_input") and self.redis_host_input:
            self.redis_host_input.setEnabled(checked)
        if hasattr(self, "redis_port_input") and self.redis_port_input:
            self.redis_port_input.setEnabled(checked)
        if hasattr(self, "redis_password_input") and self.redis_password_input:
            self.redis_password_input.setEnabled(checked)

    def load_current_settings(self):
        settings = get_app_settings()
        
        use_defaults = settings.value("gen_use_defaults", "false") == "true"
        
        curr_temp = float(settings.value("gen_temperature", 0.7))
        curr_tokens = int(settings.value("gen_max_tokens", 4096))
        
        if self.temp_input:
            self.temp_input.setValue(curr_temp)
        if self.tokens_input:
            self.tokens_input.setValue(curr_tokens)
            
        # Hydrate custom reranking config
        rerank_enabled = str(settings.value("rerank_enabled", "false")).lower() == "true"
        rerank_engine = str(settings.value("rerank_engine", "local")).lower().strip()
        rerank_endpoint = str(settings.value("rerank_endpoint", ""))
        rerank_api_key = str(settings.value("rerank_api_key", ""))
        
        if hasattr(self, "rerank_enable_cb"):
            self.rerank_enable_cb.setChecked(rerank_enabled)
            
            # Match engine index
            engine_idx = 0
            if rerank_engine == "cloud_cohere":
                engine_idx = 1
            elif rerank_engine == "cloud_custom":
                engine_idx = 2
            self.rerank_engine_combo.setCurrentIndex(engine_idx)
            
            self.rerank_endpoint_input.setText(rerank_endpoint)
            self.rerank_key_input.setText(rerank_api_key)
            
            # Fire initial visibility states
            self.on_rerank_enabled_toggled(rerank_enabled)
            
        # Hydrate Redis config
        if hasattr(self, "redis_enable_cb") and self.redis_enable_cb:
            redis_enabled = str(settings.value("redis_enabled", "false")).lower() == "true"
            redis_host = str(settings.value("redis_host", "127.0.0.1"))
            redis_port = int(settings.value("redis_port", 6379))
            redis_password = str(settings.value("redis_password", ""))
            
            self.redis_enable_cb.setChecked(redis_enabled)
            self.redis_host_input.setText(redis_host)
            self.redis_port_input.setValue(redis_port)
            self.redis_password_input.setText(redis_password)
            
            # Fire initial visibility states
            self.on_redis_enabled_toggled(redis_enabled)

        # Hydrate logging config
        if hasattr(self, "log_enable_cb") and self.log_enable_cb:
            log_enabled = str(settings.value("logging/enable_log", "false")).lower() == "true"
            debug_enabled = str(settings.value("logging/enable_debug", "false")).lower() == "true"
            self.log_enable_cb.setChecked(log_enabled)
            self.debug_enable_cb.setChecked(debug_enabled)
            
        # Hydrate SSH config
        if hasattr(self, "ssh_enable_cb") and self.ssh_enable_cb:
            ssh_enabled = str(settings.value("ssh_enabled", "false")).lower() == "true"
            ssh_host = str(settings.value("ssh_host", ""))
            ssh_port = int(settings.value("ssh_port", 22))
            ssh_user = str(settings.value("ssh_user", ""))
            
            ssh_pass_raw = str(settings.value("ssh_pass", ""))
            ssh_pass = ""
            try:
                import keyring
                if ssh_pass_raw == "KEYRING_STORED":
                    ssh_pass = keyring.get_password("SynoraStudio", "ssh_pass") or ""
                elif ssh_pass_raw:
                    import base64
                    ssh_pass = base64.b64decode(ssh_pass_raw.encode()).decode()
            except ImportError:
                if ssh_pass_raw and ssh_pass_raw != "KEYRING_STORED":
                    import base64
                    ssh_pass = base64.b64decode(ssh_pass_raw.encode()).decode()

            ssh_key = str(settings.value("ssh_key", ""))
            
            ssh_key_pass_raw = str(settings.value("ssh_key_pass", ""))
            ssh_key_pass = ""
            try:
                import keyring
                if ssh_key_pass_raw == "KEYRING_STORED":
                    ssh_key_pass = keyring.get_password("SynoraStudio", "ssh_key_pass") or ""
                elif ssh_key_pass_raw:
                    import base64
                    ssh_key_pass = base64.b64decode(ssh_key_pass_raw.encode()).decode()
            except ImportError:
                if ssh_key_pass_raw and ssh_key_pass_raw != "KEYRING_STORED":
                    import base64
                    ssh_key_pass = base64.b64decode(ssh_key_pass_raw.encode()).decode()
            
            self.ssh_enable_cb.setChecked(ssh_enabled)
            self.ssh_host_input.setText(ssh_host)
            self.ssh_port_input.setValue(ssh_port)
            self.ssh_user_input.setText(ssh_user)
            if hasattr(self, "ssh_pass_input") and self.ssh_pass_input:
                self.ssh_pass_input.setText(ssh_pass)
            self.ssh_key_input.setText(ssh_key)
            if hasattr(self, "ssh_key_pass_input") and self.ssh_key_pass_input:
                self.ssh_key_pass_input.setText(ssh_key_pass)
            
            self.on_ssh_enabled_toggled(ssh_enabled)
        
        if use_defaults:
            if self.preset_combo:
                self.preset_combo.setCurrentIndex(4)
            if self.temp_input:
                self.temp_input.setEnabled(False)
            if self.tokens_input:
                self.tokens_input.setEnabled(False)
            if self.temp_desc:
                self.temp_desc.setText("☁️ Using remote cloud baseline. No overrides active.")
            if self.token_desc:
                self.token_desc.setText("☁️ Using remote cloud baseline. No overrides active.")
        else:
            # Initialize explanations
            self.update_temp_explanation(curr_temp)
            self.update_tokens_explanation(curr_tokens)
        
    def update_temp_explanation(self, val):
        if val <= 0.2:
            desc = "💡 **Precise**: Strictly factual and deterministic. Best for pure computer code and math."
        elif val <= 0.5:
            desc = "⚖️ **Coherent**: Mostly factual with very slight linguistic variety. Good for formal business summaries."
        elif val <= 0.8:
            desc = "🤝 **Balanced**: Standard defaults. Mix of precision and human-like variation. Best all-rounder."
        elif val <= 1.2:
            desc = "🎨 **Creative**: High variance and colorful vocabulary. Best for fiction, storytelling, and brainstorming."
        else:
            desc = "🔥 **Experimental**: Total chaos. Highly random and unpredictable. Useful for avant-garde conceptual generation."
        
        self.temp_desc.setText(desc)
        
        # Reset to "Custom" preset if inputs were touched manually
        if self.sender() == self.temp_input:
            self.preset_combo.blockSignals(True)
            self.preset_combo.setCurrentIndex(0) # Set back to "Custom"
            self.preset_combo.blockSignals(False)

    def update_tokens_explanation(self, val):
        desc = f"📏 Sets the ceiling for response length. Selected capacity provides about ~{int(val * 0.75)} English words max."
        self.token_desc.setText(desc)
        
        if self.sender() == self.tokens_input:
            self.preset_combo.blockSignals(True)
            self.preset_combo.setCurrentIndex(0) # "Custom"
            self.preset_combo.blockSignals(False)

    def on_preset_changed(self, index):
        # Block infinite loop feedback
        self.temp_input.blockSignals(True)
        self.tokens_input.blockSignals(True)
        
        if index == 1: # Precise
            self.temp_input.setEnabled(True)
            self.tokens_input.setEnabled(True)
            self.temp_input.setValue(0.1)
            self.tokens_input.setValue(4096)
        elif index == 2: # Balanced
            self.temp_input.setEnabled(True)
            self.tokens_input.setEnabled(True)
            self.temp_input.setValue(0.7)
            self.tokens_input.setValue(4096)
        elif index == 3: # Creative
            self.temp_input.setEnabled(True)
            self.tokens_input.setEnabled(True)
            self.temp_input.setValue(1.0)
            self.tokens_input.setValue(8192)
        elif index == 4: # Model Default (None)
            self.temp_input.setEnabled(False)
            self.tokens_input.setEnabled(False)
            self.temp_desc.setStyleSheet("color: #aaaaaa; font-style: italic; font-weight: bold;")
            self.temp_desc.setText("☁️ Using remote cloud baseline. Temperature is NOT hardcoded.")
            self.token_desc.setText("☁️ Using remote cloud baseline. Max tokens are NOT hardcoded.")
            self.temp_input.blockSignals(False)
            self.tokens_input.blockSignals(False)
            return # Skip general updates
        else: # Custom/Fallback
            self.temp_input.setEnabled(True)
            self.tokens_input.setEnabled(True)
            self.temp_desc.setStyleSheet("color: #aaaaaa; font-style: italic;")
            
        self.temp_input.blockSignals(False)
        self.tokens_input.blockSignals(False)
        
        # Force description updates
        self.update_temp_explanation(self.temp_input.value())
        self.update_tokens_explanation(self.tokens_input.value())

    def save_and_close(self):
        settings = get_app_settings()
        is_default_mode = self.preset_combo.currentIndex() == 4 if self.preset_combo else False
        
        settings.setValue("gen_use_defaults", "true" if is_default_mode else "false")
        if self.temp_input:
            settings.setValue("gen_temperature", self.temp_input.value())
        if self.tokens_input:
            settings.setValue("gen_max_tokens", self.tokens_input.value())
            
        # Commit custom reranking changes
        if hasattr(self, "rerank_enable_cb"):
            settings.setValue("rerank_enabled", "true" if self.rerank_enable_cb.isChecked() else "false")
            
            engine_map = {0: "local", 1: "cloud_cohere", 2: "cloud_custom"}
            idx = self.rerank_engine_combo.currentIndex()
            settings.setValue("rerank_engine", engine_map.get(idx, "local"))
            
            settings.setValue("rerank_endpoint", self.rerank_endpoint_input.text().strip())
            settings.setValue("rerank_api_key", self.rerank_key_input.text().strip())
            
        # Commit logging changes
        if hasattr(self, "log_enable_cb") and self.log_enable_cb:
            settings.setValue("logging/enable_log", "true" if self.log_enable_cb.isChecked() else "false")
            settings.setValue("logging/enable_debug", "true" if self.debug_enable_cb.isChecked() else "false")
            try:
                from synora_server.utils.logger import AppLogger
                AppLogger.get_instance().reconfigure()
            except ImportError:
                pass
            
        # Commit Redis changes
        if hasattr(self, "redis_enable_cb") and self.redis_enable_cb:
            settings.setValue("redis_enabled", "true" if self.redis_enable_cb.isChecked() else "false")
            settings.setValue("redis_host", self.redis_host_input.text().strip())
            settings.setValue("redis_port", self.redis_port_input.value())
            settings.setValue("redis_password", self.redis_password_input.text().strip())
            
            # Dynamically apply config to active Redis & Event Bus services
            try:
                from synora_server.logic.services.base_service import ServiceRegistry
                redis_svc = ServiceRegistry.get("redis")
                event_bus_svc = ServiceRegistry.get("event_bus")
                
                # Graceful shutdown followed by re-initialization with new parameters
                event_bus_svc.shutdown()
                redis_svc.shutdown()
                
                redis_svc.initialize()
                event_bus_svc.initialize()
                
                # Feedback notice on the chat view if parent exists
                if self.parent() and hasattr(self.parent(), "chat_view"):
                    state_msg = "🟢 Redis central connection established." if redis_svc.is_live() else "🟡 Redis operating in offline-mock fallback."
                    self.parent().chat_view.add_system_message(f"⚙️ Redis settings updated. {state_msg}")
            except Exception as e:
                import logging
                logging.getLogger("SynoraRedisUI").error(f"Failed to dynamically apply new Redis configuration: {str(e)}")
                
        # Commit SSH changes
        if hasattr(self, "ssh_enable_cb") and self.ssh_enable_cb:
            settings.setValue("ssh_enabled", "true" if self.ssh_enable_cb.isChecked() else "false")
            settings.setValue("ssh_host", self.ssh_host_input.text().strip())
            settings.setValue("ssh_port", self.ssh_port_input.value())
            settings.setValue("ssh_user", self.ssh_user_input.text().strip())
            
            if hasattr(self, "ssh_pass_input") and self.ssh_pass_input:
                raw_pass = self.ssh_pass_input.text().strip()
                if raw_pass:
                    try:
                        import keyring
                        keyring.set_password("SynoraStudio", "ssh_pass", raw_pass)
                        settings.setValue("ssh_pass", "KEYRING_STORED")
                    except ImportError:
                        import base64
                        settings.setValue("ssh_pass", base64.b64encode(raw_pass.encode()).decode())
                else:
                    settings.setValue("ssh_pass", "")
                    
            settings.setValue("ssh_key", self.ssh_key_input.text().strip())
            
            if hasattr(self, "ssh_key_pass_input") and self.ssh_key_pass_input:
                raw_key_pass = self.ssh_key_pass_input.text().strip()
                if raw_key_pass:
                    try:
                        import keyring
                        keyring.set_password("SynoraStudio", "ssh_key_pass", raw_key_pass)
                        settings.setValue("ssh_key_pass", "KEYRING_STORED")
                    except ImportError:
                        import base64
                        settings.setValue("ssh_key_pass", base64.b64encode(raw_key_pass.encode()).decode())
                else:
                    settings.setValue("ssh_key_pass", "")
            
        # Commit SaaS Connection
        if hasattr(self, "saas_host_input") and self.saas_host_input:
            settings.setValue("saas_host_url", self.saas_host_input.text().strip())
        if hasattr(self, "saas_token_input") and self.saas_token_input:
            settings.setValue("saas_access_token", self.saas_token_input.text().strip())
            
        self.accept()

