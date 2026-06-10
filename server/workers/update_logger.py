# server/workers/update_logger.py
# Module containing classes: UpdateLogger, functions: get_logger, add_log, get_logs.

from PySide6.QtCore import QObject, Signal
from datetime import datetime
from pathlib import Path

from server.utils.path_utils import get_resource_path

class UpdateLogger(QObject):
    new_log = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.log_file = get_resource_path("resources/update_log.txt")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Create empty log file if it doesn't exist
        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")  # Create empty file

        self.logs = []
        
    def add_log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Don't truncate the message - keep full length
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)
        self.new_log.emit(log_entry)
        
        # Write full message to file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def get_logs(self):
        return self.logs
    
    def clear(self):
        self.logs = []
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("")
        self.add_log("Log cleared", "SYSTEM")

# Singleton instance
_logger_instance = None

def get_logger():
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = UpdateLogger()
    return _logger_instance
