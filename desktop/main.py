# desktop/main.py
# Module containing functions: detect_environment, smart_sync, copy_bundled_resources.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# main.py
# This is the main entry point for the Synora Studio. It initializes the application and shows the main window.  
import sys
import os
import platform

# 1. SET APP IDENTITY (Windows Taskbar Grouping) - MUST BE SET BEFORE ANY QT GUI CLASS/DLL INITS
if platform.system() == "Windows":
    import ctypes
    myappid = 'arean82.synorastudio.v9.0'
    try:
        # Explicitly declare argument and return types for wide-string (Unicode) translation
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID.argtypes = [ctypes.c_wchar_p]
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID.restype = ctypes.c_long
        res = ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        print(f"[Icon Loader] Windows AppUserModelID set to '{myappid}' successfully at script startup. Result: {res}")
    except Exception as e:
        print(f"[Icon Loader] Warning: Failed to set AppUserModelID at script startup: {e}")

import shutil
from pathlib import Path

# --- Auto-Cleanup Block (Moves files improperly placed in root) ---
try:
    _root = Path(__file__).parent
    
    def safe_move(src_name, dst_dir_name, dst_file_name):
        src = _root / src_name
        dst_dir = _root / dst_dir_name
        dst = dst_dir / dst_file_name
        if src.exists():
            dst_dir.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(str(src), str(dst))
                os.remove(str(src))
                
    safe_move("saas_tenants.db", "data", "saas_tenants.db")
    safe_move("reset_admin.py", "operator_tools/admin_reset", "reset_admin.py")
    safe_move("test_reranker.py", "scratch", "test_reranker.py")
except OSError as e: 
    import logging
    logging.error(f"Auto-cleanup failed (OS Error): {e}")
# -----------------------------------------------------------------

from server.utils.path_utils import get_resource_path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Top-level PySide6 graphical imports removed for strict headless bypass (7.1.1)
from PySide6.QtCore import QFile, QIODevice

# from ui.main_window import MainWindowClass (Moved to main() for headless safety)
# ChatWorker import removed (handled by HeadlessEngine)

def detect_environment():
    """
    Logic: Intelligently auto-detect if running in a Headless/CLI environment or a GUI environment.
    - Explicit flags override: --headless or --cli.
    - Docker: Checks for .dockerenv or DOCKER_CONTAINER.
    - Linux: Checks for 'DISPLAY' or 'WAYLAND_DISPLAY'.
    - SSH/TTY Check: Detects running in SSH terminals or non-interactive container services.
    """
    if "--headless" in sys.argv:
        return "HEADLESS"
    if "--cli" in sys.argv:
        return "CLI"
    if "--list-models" in sys.argv or "--update-models" in sys.argv:
        return "CLI"
        
    # Check Docker Container explicitly
    if os.path.exists("/.dockerenv") or os.environ.get("DOCKER_CONTAINER"):
        return "HEADLESS"
        
    # Check Linux displays
    if sys.platform == "linux" and not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
        return "HEADLESS"
        
    # Check if running under SSH terminal
    if os.environ.get("SSH_CLIENT") or os.environ.get("SSH_TTY"):
        return "CLI" if sys.stdin and sys.stdin.isatty() else "HEADLESS"
        
    return "GUI"


def smart_sync(src: Path, dst: Path):
    """Only copies src to dst if dst is missing or src is newer/different."""
    if not src.exists():
        return False
    
    should_copy = False
    if not dst.exists():
        should_copy = True
    else:
        # Compare modification times and sizes
        src_stat = src.stat()
        dst_stat = dst.stat()
        if src_stat.st_mtime > dst_stat.st_mtime or src_stat.st_size != dst_stat.st_size:
            should_copy = True
            
    if should_copy:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    return False

def copy_bundled_resources():
    """
    Handles resource synchronization for the EXE environment.
    - System Files: Updated only if the version in the EXE is newer.
    - User Files: Created only if missing.
    """
    if not getattr(sys, 'frozen', False):
        return
    
    try:
        from server.utils.storage_config import StorageManager
        bundle_dir = Path(sys._MEIPASS)
        # Crucial Fix: Extract into the verified writable storage path, not the EXE folder
        target_root = StorageManager.get_instance().get_storage_root()
        
        # 1. SYSTEM FILES & UI DESIGNER: Smart Sync (ensures updates without full wipe)
        system_files = [
            'resources/styles.qss',
            'resources/app_icon.png',
            'resources/app_icon.ico',
            'resources/app_icon.icns',
            'resources/app_icon_linux.png',
        ]
        
        for rel_path in system_files:
            smart_sync(bundle_dir / rel_path, target_root / rel_path)

        # Sync the entire UI designer folder individually
        bundle_ui = bundle_dir / "ui_designer"
        target_ui = target_root / "ui_designer"
        if bundle_ui.exists():
            for src_file in bundle_ui.rglob("*"):
                if src_file.is_file():
                    rel_path = src_file.relative_to(bundle_ui)
                    smart_sync(src_file, target_ui / rel_path)

        # 2. USER FILES: Only copy if MISSING (protects user work)
        # Dynamically sync any models_*.json files present in bundle
        bundle_res = bundle_dir / "resources"
        target_res = target_root / "resources"
        
        if bundle_res.exists():
            # Find all model manifests
            for src_file in bundle_res.glob("models_*.json"):
                dst_file = target_res / src_file.name
                if not dst_file.exists():
                    target_res.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
            
            # Handle specific fallback files
            legacy_files = ['models.json', 'user_prompts.json']
            for fname in legacy_files:
                src = bundle_res / fname
                dst = target_res / fname
                if src.exists() and not dst.exists():
                    target_res.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                
    except Exception as e:
        print(f"Resource sync error: {e}")

def main():
    # Detect Mode (GUI or Headless)
    env_mode = detect_environment()
    
    import sys
    from PySide6.QtCore import QSettings
    
    from server.utils.storage_config import StorageManager
    from server.utils.logger import AppLogger
    
    manager = StorageManager.get_instance()
    
    # Initialize Core Telemetry Logger
    logger = AppLogger.get_instance()
    logger.info("Synora Studio SaaS Multi-Tenant Cloud Platform initializing...")
    
    # Create the App instance first so we can apply styles/icons to it (safely wrapped)
    app = None
    if env_mode == "GUI":
        try:
            from PySide6.QtWidgets import QApplication
            app = QApplication(sys.argv)
        except Exception as e:
            print(f"[*] Warning: Graphical Display server unavailable or failed to connect ({e}).")
            print("[*] Automatically falling back to Headless Engine mode.")
            env_mode = "HEADLESS"
            
        # 2. APPLY GLOBAL ICON
        from desktop.ui.shared_widgets import set_app_icon
        set_app_icon(app)

        # 3. LOAD STYLES
        from server.utils.path_utils import get_resource_path
        app.setStyle("Fusion")
        
    # Ensure QCoreApplication exists for Headless / CLI threads to avoid "QCoreApplication must be created before QObject"
    if not app:
        from PySide6.QtCore import QCoreApplication
        app = QCoreApplication.instance() or QCoreApplication(sys.argv)
    
    # --- SINGLE INSTANCE LOCK (Restored from v6) ---
    from PySide6.QtCore import QLockFile, QDir, QStandardPaths
    lock_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    os.makedirs(lock_dir, exist_ok=True)
    lock_path = os.path.join(lock_dir, "synorastudio.lock")
    lock_file = QLockFile(lock_path)
    if not lock_file.tryLock(500):
        if env_mode == "GUI":
            from PySide6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Already Running")
            msg.setText("Another instance of Synora Studio is already running.")
            msg.setInformativeText("Please close the existing instance before launching a new one.")
            msg.exec()
        else:
            print("[!] Error: Another instance of Synora Studio is already running.")
        return
    
    # --- STORAGE CONFIGURATION LAYER ---
    from server.utils.storage_config import StorageManager
    from desktop.ui.first_run_dialog import FirstRunDialog
    from PySide6.QtCore import QSettings
    
    manager = StorageManager.get_instance()
    
    # Perform permission-based mode detection
    if manager.detect_existing_mode() is None:
        if env_mode == "GUI":
            setup_dlg = FirstRunDialog()
            if setup_dlg.exec() != FirstRunDialog.Accepted:
                sys.exit(0)
        else:
            # Headless default to APPDATA if not configured
            manager.finalize_setup("APPDATA")
            
    # GLORIOUS GLOBAL SWITCHER:
    # If we are portable, we override default QSettings storage globally to prevent Registry writes.
    if manager.is_portable:
        QSettings.setDefaultFormat(QSettings.IniFormat)
        # Explicitly set the scope path to the verified writable target root.
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, str(manager.get_storage_root()))
    
    # Now copy files safely without permission crash
    copy_bundled_resources()
    
    if env_mode == "GUI":
        from desktop.ui.main_window import MainWindowClass
        # Load stylesheet - use get_resource_path
        stylesheet_path = get_resource_path("resources/styles.qss")
        if stylesheet_path.exists():
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
                
        # Apply Global Application Icon (ALREADY HANDLED AT TOP)
        # from ui.shared_widgets import set_app_icon
        # set_app_icon(app) 
        
    # CLI Command Router
    if "--help" in sys.argv or "-h" in sys.argv:
        print("\n" + "="*50)
        print(" LLM CHAT APP - Headless Engine v9.0")
        print("="*50)
        print("Usage: python main.py [options]")
        print("\nOptions:")
        print("  --cli             Launch the interactive terminal chat session")
        print("  --list-models     List all models currently in the local manifest")
        print("  --update-models   Fetch latest models from the active provider")
        print("  --migrate         Migrate chat history transactionally between databases")
        print("  --reset-admin     Reset the SaaS admin credentials to default")
        print("  --api-manager     Manage the Local API Server (Port 5000) settings interactively")
        print("  --help / -h       Show this detailed help message")
        
        print("\nExamples:")
        print("  1. Sync Models:     python main.py --update-models")
        print("  3. View manifest:   python main.py --list-models")
        print("  4. CLI Chat:        python main.py --cli")
        print("  5. Relocate DB:     python main.py --migrate")
        
        print("\nDocumentation: see HEADLESS_GUIDE.md")
        print("="*50 + "\n")
        return

    if "--list-models" in sys.argv:
        from desktop.headless.models import HeadlessModels
        HeadlessModels.list_models()
        return

    if "--update-models" in sys.argv:
        from server.logic.llm_client import LLMClient
        from desktop.headless.models import HeadlessModels
        client = LLMClient()
        client.hydrate()
        HeadlessModels.update_models(client)
        return

    if "--migrate" in sys.argv:
        from server.logic.migration_bridge import run_interactive_cli_migration
        run_interactive_cli_migration()
        return
        
    if "--reset-admin" in sys.argv:
        from scripts.reset_admin import reset_admin
        reset_admin()
        return

    if "--api-manager" in sys.argv:
        from desktop.core.settings_controller import SettingsController
        SettingsController.run_api_manager()
        return

    if env_mode == "CLI" or "--cli" in sys.argv:
        from desktop.core.chat_controller import ChatController
        ChatController.run_cli_chat()
        return

    if env_mode == "HEADLESS" or "--headless" in sys.argv:
        print("[!] The standalone API server has been moved to 'server/run_server.py'.")
        print("[!] Please run: python server/run_server.py")
        sys.exit(1)
    else:
        # --- GUI EXECUTION PATH ---
        from desktop.core.auth_controller import AuthController
        AuthController.run_gui_auth()
            
        # INITIALIZE MAIN WINDOW
        from desktop.ui.main_window import MainWindowClass
        window = MainWindowClass()
        window.showMaximized()  
        window.start_services()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
