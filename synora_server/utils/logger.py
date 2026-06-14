# synora_server/utils/logger.py
# Module containing classes: PrintLogger, AppLogger, functions: write, flush, get_instance.

import sys
import logging
import json
import requests
import threading
from datetime import datetime, timezone
from pathlib import Path
from synora_server.utils.storage_config import StorageManager

class PrintLogger:
    """Redirects print statements to the central logger if debug prints are enabled."""
    def __init__(self, logger, original_stdout):
        self.logger = logger
        self.original_stdout = original_stdout

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.debug(line.strip())
        self.original_stdout.write(buf)

    def flush(self):
        self.original_stdout.flush()

class AppLogger:
    _instance = None

    @classmethod
    def get_instance(cls, component_name="app"):
        if cls._instance is None:
            cls._instance = AppLogger(component_name)
        return cls._instance

    def __init__(self, component_name="app"):
        self.component_name = component_name
        self.logger = logging.getLogger(f"SynoraApp_{component_name}")
        self.logger.propagate = False
        self.formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        
        self.file_handler = None
        self.siem_file_handler = None
        self._original_stdout = sys.stdout
        self._hooked = False
        
        self.reconfigure()

    def reconfigure(self):
        settings = StorageManager.get_instance().get_active_settings()
        enable_log = str(settings.value("logging/enable_log", "false")).lower() == "true"
        enable_debug = str(settings.value("logging/enable_debug", "false")).lower() == "true"
        
        level = logging.DEBUG if enable_debug else logging.INFO
        self.logger.setLevel(level)
        self.console_handler.setLevel(level)
        
        # Handle file writing
        if enable_log:
            if not self.file_handler:
                storage_root = StorageManager.get_instance().get_storage_root()
                log_dir = storage_root / "logs" / self.component_name
                log_dir.mkdir(parents=True, exist_ok=True)
                log_file = log_dir / f"{self.component_name}.log"
                
                self.file_handler = logging.FileHandler(str(log_file), encoding='utf-8')
                self.file_handler.setFormatter(self.formatter)
                self.logger.addHandler(self.file_handler)
            self.file_handler.setLevel(level)
        else:
            if self.file_handler:
                self.logger.removeHandler(self.file_handler)
                self.file_handler.close()
                self.file_handler = None
                
        # Handle SIEM File Logging
        siem_enabled = str(settings.value("siem/enable", "false")).lower() == "true"
        siem_file_log = str(settings.value("siem/file_logging", "true")).lower() == "true"
        
        if siem_enabled and siem_file_log:
            if not self.siem_file_handler:
                storage_root = StorageManager.get_instance().get_storage_root()
                siem_dir = storage_root / "logs" / "siem"
                siem_dir.mkdir(parents=True, exist_ok=True)
                siem_file = siem_dir / "audit.jsonl"
                
                self.siem_file_handler = logging.FileHandler(str(siem_file), encoding='utf-8')
                # Strict JSONL formatter
                self.siem_file_handler.setFormatter(logging.Formatter('%(message)s'))
        else:
            if self.siem_file_handler:
                self.siem_file_handler.close()
                self.siem_file_handler = None
                
        # Hook global stdout for debug prints
        if enable_debug and enable_log and not self._hooked:
            sys.stdout = PrintLogger(self.logger, self._original_stdout)
            self._hooked = True
        elif not (enable_debug and enable_log) and self._hooked:
            sys.stdout = self._original_stdout
            self._hooked = False

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
        
    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def siem_audit(self, event_type, user, action, metadata=None):
        settings = StorageManager.get_instance().get_active_settings()
        if str(settings.value("siem/enable", "false")).lower() != "true":
            return
            
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "user": user,
            "action": action,
            "metadata": metadata or {},
            "component": self.component_name
        }
        json_payload = json.dumps(payload)
        
        # 1. Write to local JSONL if enabled
        if self.siem_file_handler:
            self.siem_file_handler.emit(logging.LogRecord(
                name="SIEM", level=logging.INFO, pathname="", lineno=0, msg=json_payload, args=(), exc_info=None
            ))
            
        # 2. Fire-and-forget HTTP Webhook if configured
        webhook_url = str(settings.value("siem/webhook_url", ""))
        if webhook_url and webhook_url.startswith("http"):
            def send_webhook():
                try:
                    requests.post(webhook_url, json=payload, timeout=3)
                except Exception as e:
                    self.error(f"SIEM Webhook delivery failed: {e}")
            threading.Thread(target=send_webhook, daemon=True).start()
