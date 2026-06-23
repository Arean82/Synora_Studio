# synora_saas/core/app.py
# Module containing classes: SaaSServer, functions: create_saas_app, get_locale, handle_join.

import sys
import os
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, Response, stream_with_context, render_template, send_from_directory, g
from flask_babel import Babel
from flask_socketio import SocketIO, join_room

# Set path context for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from synora_server.logic.model_io import load_provider_metadata
from synora_server.utils import get_resource_path
from synora_server.utils.security_utils import admin_required
from synora_server.logic.tenant.tenant_db import TenantDatabaseManager
from synora_server.logic.llm_client import LLMClient
from synora_server.utils.storage_config import StorageManager
from PySide6.QtCore import QThread, Signal

# Import Modular Routes
from synora_saas.routes import (
    register_auth_routes,
    register_admin_routes,
    register_api_routes,
    register_dashboard_routes,
    register_system_routes
)

socketio = SocketIO(cors_allowed_origins="*")

def create_saas_app():
    from synora_server.utils.logger import AppLogger
    logger = AppLogger.get_instance("synora_saas")
    logger.info("Initializing SaaS Web Portal...")
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    import mimetypes
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales'))
    
    def get_locale():
        return request.accept_languages.best_match(['en', 'es', 'fr', 'de'])
        
    babel = Babel(app, locale_selector=get_locale)
    db = TenantDatabaseManager()
    
    socketio.init_app(app)
    
    @socketio.on('join')
    def handle_join(data):
        user_id = data.get('user_id')
        if user_id:
            join_room(user_id)
            print(f"[Socket.IO] Authenticated client joined room: {user_id}")
    
    def send_alert_email(to_email, subject, html_content):
        try:
            from synora_server.logic.tenant.config_manager import SaaSConfigManager
            saas_cfg = SaaSConfigManager()
            
            if not saas_cfg.get_bool("SMTP_RELAY", "enabled", False):
                return False
                
            smtp_host = saas_cfg.get_str("SMTP_RELAY", "host", "smtp.gmail.com")
            smtp_port = saas_cfg.get_int("SMTP_RELAY", "port", 587)
            smtp_user = saas_cfg.get_str("SMTP_RELAY", "user", "")
            smtp_pass = saas_cfg.get_str("SMTP_RELAY", "password", "")
            sender_name = saas_cfg.get_str("SMTP_RELAY", "sender_name", "Synora Studio Security")
            sender_email = saas_cfg.get_str("SMTP_RELAY", "sender_email", "alertbot@synorastudio.local")
            
            if not smtp_user or not smtp_pass:
                return False
                
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{sender_name} <{sender_email}>"
            msg["To"] = to_email
            msg.attach(MIMEText(html_content, "html"))
            
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender_email, to_email, msg.as_string())
            return True
        except Exception as e:
            print(f"[SMTP Warning]: Autonomous alert failed: {e}")
            return False

    def get_provider_base_url(provider_id: str) -> str:
        default_urls = {
            "nvidia": "https://integrate.api.nvidia.com/v1",
            "openai": "https://api.openai.com/v1",
            "groq": "https://api.groq.com/openai/v1",
            "lmstudio": "http://localhost:1234/v1",
            "ollama": "http://localhost:11434/v1"
        }
        try:
            from synora_server.utils.path_utils import get_resource_path
            conf_path = get_resource_path("resources/api_providers.json")
            if os.path.exists(conf_path):
                with open(conf_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for p in data.get("providers", []):
                        if p.get("id") == provider_id:
                            return p.get("default_url", default_urls.get(provider_id, "https://integrate.api.nvidia.com/v1"))
        except Exception as e:
            print(f"[API Warning]: URL provider lookup failed: {e}")
        return default_urls.get(provider_id, "https://integrate.api.nvidia.com/v1")

    @app.route('/app_icon.ico')
    @app.route('/favicon.ico')
    def serve_favicon():
        resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'synora_server', 'resources'))
        return send_from_directory(resources_dir, 'app_icon.ico')

    @app.before_request
    def record_start_time():
        request.start_time = time.perf_counter()

    @app.after_request
    def log_telemetry_metrics(response):
        exempt_starts = ['/static', '/health', '/app_icon.ico', '/favicon.ico']
        if any(request.path.startswith(prefix) for prefix in exempt_starts):
            return response
            
        start_time = getattr(request, 'start_time', None)
        if start_time:
            latency = time.perf_counter() - start_time
            user = getattr(request, 'tenant', None)
            tenant_id = user['id'] if user else "anonymous"
            
            tokens = 0
            if request.path == '/v1/chat/completions' and response.status_code == 200:
                try:
                    data = request.get_json(silent=True) or {}
                    messages = data.get("messages", [])
                    prompt_chars = sum(len(m.get("content", "")) for m in messages)
                    tokens = int(prompt_chars / 4)
                except:
                    pass
            
            error = (response.status_code >= 400)
            
            try:
                from synora_server.logic.services import ServiceRegistry
                telemetry_service = ServiceRegistry.get("telemetry")
                import threading
                threading.Thread(target=telemetry_service.record_request, kwargs={
                    "tenant_id": str(tenant_id),
                    "latency": latency,
                    "tokens": tokens,
                    "error": error
                }, daemon=True).start()
            except:
                pass
                
        return response

    @app.before_request
    def enforce_tenant_authorization():
        exempt_starts = ['/static', '/health', '/api/validate_passport', '/api/register', '/api/login', '/app_icon.ico', '/favicon.ico']
        exempt_starts += ['/v1/health', '/v2/health', '/v1/validate_passport', '/v2/validate_passport', 
                         '/v1/register', '/v2/register', '/v1/login', '/v2/login']
                         
        if request.path == '/' or any(request.path.startswith(prefix) for prefix in exempt_starts):
            return None
            
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized. Missing API Passport token."}), 401
            
        passport_key = auth_header.replace("Bearer ", "").strip()
        
        user = None
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            payload = auth_service.verify_token(passport_key)
            if payload:
                user = {
                    "id": payload["id"],
                    "username": payload["username"],
                    "email": payload["email"],
                    "key_type": payload["key_type"],
                    "api_key": passport_key,
                    "status": "active"
                }
        except Exception as e: 
            user = None

        if not user:
            user = db.authenticate_by_passport(passport_key)
        
        if not user:
            return jsonify({"error": "Forbidden. Invalid or revoked API Passport."}), 403
            
        request.tenant = user

        try:
            from synora_server.logic.services import ServiceRegistry
            rate_limiter = ServiceRegistry.get("rate_limiter")
            
            ip = request.remote_addr or "unknown_ip"
            if not rate_limiter.is_allowed(f"ip:{ip}", limit=120):
                try:
                    telemetry_service = ServiceRegistry.get("telemetry")
                    if telemetry_service:
                        telemetry_service.record_rate_limit_block()
                except Exception as e: 
                    pass
                return jsonify({"error": "Too Many Requests", "message": "Global IP rate limit exceeded."}), 429

            settings = db.get_user_settings(user['id'])
            rpm_limit = int(settings.get("requests_per_minute_limit", 60 if user['username'] != 'admin' else 0))
            if rpm_limit > 0:
                if not rate_limiter.is_allowed(f"tenant:{user['id']}", limit=rpm_limit):
                    try:
                        telemetry_service = ServiceRegistry.get("telemetry")
                        if telemetry_service:
                            telemetry_service.record_rate_limit_block()
                    except Exception as e: 
                        pass
                    return jsonify({"error": "Too Many Requests", "message": f"Tenant rate limit of {rpm_limit} RPM exceeded."}), 429
        except Exception as e:
            pass

        return None

    # Register modular routes
    register_auth_routes(app, db, send_alert_email)
    register_admin_routes(app, db)
    register_api_routes(app, db, get_provider_base_url)
    register_dashboard_routes(app, db)
    register_system_routes(app)

    return app

class SaaSServer(QThread):
    status_changed = Signal(bool, str)
    api_manager_action = Signal(str)

    def __init__(self, host: str = '127.0.0.1', port: int = 5000, parent=None):
        super().__init__(parent)
        self.flask_app = create_saas_app()
        self.flask_app.saas_server_instance = self
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        self._startup_error = None

    def start_server(self):
        if self.running:
            return True, "Already active"
            
        import socket
        bind_address = '127.0.0.1' if self.host == 'localhost' else self.host
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((bind_address, self.port))
            except OSError:
                msg = f"Port {self.port} is currently tied by another service."
                return False, msg
                
        try:
            from werkzeug.serving import make_server
            self.server = make_server(bind_address, self.port, self.flask_app, threaded=True)
            self.running = True
            super().start()
            return True, "Success"
        except Exception as e:
            return False, f"Runtime Fault: {str(e)}"

    def run(self):
        print(f"[SaaS Daemon] Background server established at http://{self.host}:{self.port}")
        if self.server:
            self.server.serve_forever()

    def stop(self):
        if self.server:
            print("[SaaS Daemon] Commencing soft shutdown sequence...")
            self.server.shutdown()
            self.server = None
        self.running = False
        self.quit()
        self.wait()
        return True
