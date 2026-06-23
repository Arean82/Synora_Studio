# synora_saas/routes/auth_routes.py
# Module containing functions: register_auth_routes, validate_passport, register_user.

import os
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, jsonify

_RESET_TOKENS = {}

def register_auth_routes(app, db, send_alert_email):

    @app.route('/api/validate_passport', methods=['POST'])
    @app.route('/v1/validate_passport', methods=['POST'])
    @app.route('/v2/validate_passport', methods=['POST'])
    def validate_passport():
        data = request.get_json(silent=True) or {}
        api_key = data.get("api_key", "").strip()
        provider = data.get("provider", "nvidia").lower()
        
        if not api_key:
            return jsonify({"success": False, "error": "API Key passport required."}), 400
            
        try:
            from openai import OpenAI
            base_url = "https://integrate.api.nvidia.com/v1" if provider == "nvidia" else "https://api.openai.com/v1"
            
            temp_client = OpenAI(base_url=base_url, api_key=api_key, timeout=8.0)
            temp_client.models.list()
            
            return jsonify({
                "success": True, 
                "status": "validated", 
                "message": "Passport verified active. Form unlocked for profile registration."
            })
        except Exception as e:
            return jsonify({
                "success": False, 
                "error": f"Passport Validation Failed: {str(e)}"
            }), 401

    @app.route('/api/register', methods=['POST'])
    @app.route('/v1/register', methods=['POST'])
    @app.route('/v2/register', methods=['POST'])
    def register_user():
        data = request.get_json(silent=True) or {}
        api_key = data.get("api_key", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        key_type = "byok"
        
        if not all([api_key, username, email, password]):
            return jsonify({"success": False, "error": "All fields are mandatory."}), 400
            
        if key_type not in ['byok', 'admin_funded']:
            return jsonify({"success": False, "error": "Invalid user key tier classification."}), 400

        user_id, db_err = db.register_user(api_key, username, email, password, key_type)
        if db_err:
            return jsonify({"success": False, "error": db_err}), 400
            
        workspace = db.get_user_workspace(user_id)
        
        try:
            from synora_server.utils.path_utils import get_resource_path
            template_path = get_resource_path(os.path.join("data", "email_templates", "welcome.html"))
            with open(template_path, 'r', encoding='utf-8') as f:
                welcome_html = f.read()
            welcome_html = welcome_html.replace("{username}", username).replace("{key_type}", key_type.upper())
        except Exception as e:
            print(f"[Email Template Error] Could not load welcome.html: {e}")
            welcome_html = f"<h2>Welcome to the Multi-Tenant Grid, {username}!</h2><p>Your secured SaaS sandbox has been successfully provisioned.</p><p><b>Key Type Tier:</b> {key_type.upper()}</p>"
        import threading
        threading.Thread(target=send_alert_email, args=(email, "Workspace Provisoned - Synora Studio", welcome_html), daemon=True).start()

        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            user_data = {"id": user_id, "username": username, "email": email, "key_type": key_type}
            jwt_token = auth_service.generate_token(user_data)
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            jwt_token = api_key

        return jsonify({
            "success": True,
            "user_id": user_id,
            "key_type": key_type,
            "workspace_provisioned": True,
            "token": jwt_token,
            "passport_token": jwt_token,
            "message": "Multi-tenant account successfully provisioned. You may now log in."
        }), 201

    @app.route('/api/forgot_password', methods=['POST'])
    @app.route('/v1/forgot_password', methods=['POST'])
    def forgot_password():
        data = request.get_json(silent=True) or {}
        email = data.get("email", "").strip()
        
        if not email:
            return jsonify({"success": False, "error": "Email is required."}), 400
            
        with db.get_connection() as conn:
            row = conn.execute("SELECT id, username FROM users WHERE email = ?", (email,)).fetchone()
            if not row:
                # Security: Return success even if email not found to prevent user enumeration
                return jsonify({"success": True, "message": "If an account exists, a reset code has been sent."})
                
        import secrets
        otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        _RESET_TOKENS[email] = {
            "code": otp_code,
            "expires": time.time() + 600 # 10 minutes
        }
        
        # DEMO MODE SIMULATION: Print to console so the admin/user testing it can see the OTP without SMTP
        print(f"\n==========================================")
        print(f"[DEMO SIMULATION] Password Reset Triggered")
        print(f"Target Email: {email}")
        print(f"6-Digit OTP:  {otp_code}")
        print(f"==========================================\n")
        
        try:
            from synora_server.utils.path_utils import get_resource_path
            template_path = get_resource_path(os.path.join("data", "email_templates", "password_reset.html"))
            with open(template_path, 'r', encoding='utf-8') as f:
                email_html = f.read()
            email_html = email_html.replace("{otp_code}", otp_code)
        except Exception as e:
            print(f"[Email Template Error] Could not load password_reset.html: {e}")
            email_html = f"<h3>Synora Studio Password Reset</h3><p>Your password reset code is: <b style='font-size:24px; letter-spacing:2px;'>{otp_code}</b></p><p>This code expires in 10 minutes.</p>"
        import threading
        threading.Thread(target=send_alert_email, args=(email, "Password Reset Code", email_html), daemon=True).start()
        
        return jsonify({"success": True, "message": "If an account exists, a reset code has been sent."})

    @app.route('/api/reset_password', methods=['POST'])
    @app.route('/v1/reset_password', methods=['POST'])
    def reset_password():
        data = request.get_json(silent=True) or {}
        email = data.get("email", "").strip()
        code = data.get("code", "").strip()
        new_password = data.get("new_password", "").strip()
        
        if not all([email, code, new_password]):
            return jsonify({"success": False, "error": "Email, code, and new password are required."}), 400
            
        token_data = _RESET_TOKENS.get(email)
        if not token_data:
            return jsonify({"success": False, "error": "Invalid or expired reset code."}), 400
            
        if time.time() > token_data["expires"]:
            del _RESET_TOKENS[email]
            return jsonify({"success": False, "error": "Reset code has expired. Please request a new one."}), 400
            
        if token_data["code"] != code:
            return jsonify({"success": False, "error": "Incorrect reset code."}), 400
            
        with db.get_connection() as conn:
            row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            if not row:
                return jsonify({"success": False, "error": "Account not found."}), 404
            user_id = row[0]
            
        success, message = db.update_user_profile(user_id=user_id, password_raw=new_password)
        if success:
            del _RESET_TOKENS[email]
            
            # SIEM Audit
            from synora_server.utils.logger import AppLogger
            AppLogger.get_instance("synora_saas").siem_audit(
                event_type="password_reset",
                user=email,
                action="self_service_password_reset",
                metadata={"email": email}
            )
            return jsonify({"success": True, "message": "Password successfully reset. You may now log in."})
        else:
            return jsonify({"success": False, "error": message}), 500

    @app.route('/api/login', methods=['POST'])
    @app.route('/v1/login', methods=['POST'])
    @app.route('/v2/login', methods=['POST'])
    def login_user():
        data = request.get_json(silent=True) or {}
        user_input = data.get("username_or_email", "").strip()
        password = data.get("password", "").strip()
        
        user = db.authenticate_by_login(user_input, password)
        if not user:
            return jsonify({"success": False, "error": "Invalid login credentials."}), 401
            
        user['passport_token'] = user.get('api_key', '')
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            jwt_token = auth_service.generate_token(user)
            user['passport_token'] = jwt_token
            user['token'] = jwt_token
        except Exception as e:
            pass
            
        from synora_server.utils.logger import AppLogger
        AppLogger.get_instance("synora_saas").siem_audit(
            event_type="login_success",
            user=user['username'],
            action="login_success",
            metadata={"email": user['email']}
        )
            
        return jsonify({
            "success": True,
            "user": user,
            "message": f"Authentication successful. Welcome back, {user['username']}."
        })

    @app.route('/api/verify_otp', methods=['POST'])
    @app.route('/v1/verify_otp', methods=['POST'])
    def verify_otp():
        data = request.get_json(silent=True) or {}
        user_id = data.get("user_id")
        otp_code = data.get("otp_code", "").strip()
        
        if not user_id or not otp_code:
            return jsonify({"success": False, "error": "Missing user ID or OTP code."}), 400
            
        otp_secret = db.get_user_otp_secret(user_id)
        if not otp_secret:
            return jsonify({"success": False, "error": "Account lacks OTP configuration."}), 500
            
        import pyotp
        totp = pyotp.TOTP(otp_secret)
        if not totp.verify(otp_code, valid_window=2):
            return jsonify({"success": False, "error": "Invalid or expired OTP."}), 401
            
        with db.get_connection() as conn:
            row = conn.execute("SELECT id, username, email, api_key, key_type, status FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                return jsonify({"success": False, "error": "User not found."}), 404
            user = dict(row)
            user['passport_token'] = user.get('api_key', '')
            
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            jwt_token = auth_service.generate_token(user)
            user['passport_token'] = jwt_token
            user['token'] = jwt_token
        except Exception as e:
            print(f"[JWT Error] Failed to generate token: {e}")
            
        from synora_server.utils.logger import AppLogger
        AppLogger.get_instance("synora_saas").siem_audit(
            event_type="login_success",
            user=user['username'],
            action="verify_otp_success",
            metadata={"email": user['email']}
        )
            
        return jsonify({
            "success": True,
            "user": user,
            "message": f"Authentication successful. Welcome back, {user['username']}."
        })

    @app.route('/api/update_profile', methods=['POST'])
    @app.route('/v1/update_profile', methods=['POST'])
    @app.route('/v2/update_profile', methods=['POST'])
    def update_profile():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        data = request.get_json(silent=True) or {}
        new_username = data.get("username", "").strip()
        new_password = data.get("password", "").strip()
        new_api_key = data.get("api_key", "").strip()
        
        if not any([new_username, new_password, new_api_key]):
            return jsonify({"success": False, "error": "No profile update parameters provided."}), 400
            
        success, message = db.update_user_profile(user_id=user['id'], username=new_username or None, password_raw=new_password or None, api_key=new_api_key or None)
        
        if not success:
            return jsonify({"success": False, "error": message}), 400
            
        target_key = new_api_key if new_api_key else user.get('api_key')
        refreshed = db.authenticate_by_passport(target_key)
        
        if not refreshed:
            return jsonify({"success": False, "error": "Synchronized validation handshake failed."}), 500
            
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            jwt_token = auth_service.generate_token(refreshed)
            refreshed['passport_token'] = jwt_token
            refreshed['token'] = jwt_token
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            refreshed['passport_token'] = refreshed.get('api_key', '')
        
        return jsonify({
            "success": True,
            "user": refreshed,
            "message": "Local sandbox security profile successfully updated!"
        })

    @app.route('/v1/tenant/credentials', methods=['GET', 'POST'])
    @app.route('/v2/tenant/credentials', methods=['GET', 'POST'])
    def manage_credentials():
        is_admin = request.tenant['username'] == 'admin'
        
        if request.method == 'GET':
            if is_admin:
                import keyring
                import json
                from synora_server.utils.path_utils import get_app_settings
                from synora_server.logic.model_io import load_provider_metadata
                
                creds = {}
                try:
                    metadata = load_provider_metadata()
                    for p in metadata.get("providers", []):
                        pid = p.get("id")
                        if not pid: continue
                        creds[pid] = keyring.get_password("LLMChatApp", f"api_key_{pid}") or ""
                        creds[f"{pid}_base_url"] = keyring.get_password("LLMChatApp", f"url_{pid}") or ""
                        
                    custom = json.loads(get_app_settings().value("custom_providers", "[]"))
                    for c in custom:
                        eco_key = c['ecosystem'].lower().replace(' ', '_')
                        cid = f"{c['sdk']}_{eco_key}"
                        creds[cid] = keyring.get_password("LLMChatApp", f"api_key_{cid}") or ""
                        creds[f"{cid}_base_url"] = keyring.get_password("LLMChatApp", f"url_{cid}") or ""
                except:
                    pass
                    
                if not creds.get('nvidia'):
                    creds['nvidia'] = keyring.get_password("LLMChatApp", "api_key") or ""
            else:
                creds = db.get_tenant_credentials(request.tenant['id'])
                
            masked = {}
            for prov, key in creds.items():
                if not key:
                    continue
                if prov.endswith('_base_url'):
                    masked[prov] = key
                elif len(key) > 8:
                    masked[prov] = key[:4] + "...." + key[-4:]
                else:
                    masked[prov] = "********"
            return jsonify(masked)
        
        elif request.method == 'POST':
            data = request.json
            if not isinstance(data, dict):
                return jsonify({"error": "Invalid format"}), 400
                
            if is_admin:
                import keyring
                for prov, key in data.items():
                    if prov.endswith('_base_url'):
                        k_name = f"url_{prov.replace('_base_url', '')}"
                    else:
                        k_name = f"api_key_{prov}"
                    
                    if key.strip():
                        keyring.set_password("LLMChatApp", k_name, key.strip())
                    else:
                        try: keyring.delete_password("LLMChatApp", k_name)
                        except: pass
            else:
                for prov, key in data.items():
                    db.set_tenant_credential(request.tenant['id'], prov.lower(), key.strip())
            return jsonify({"status": "success", "message": "Credentials synchronized."})

    @app.route('/api/tenant/settings', methods=['GET', 'POST'])
    def manage_tenant_settings():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
            
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            
            if request.method == 'GET':
                settings = auth_service.get_user_settings(user['id'])
                return jsonify({"success": True, "settings": settings})
                
            if request.method == 'POST':
                new_settings = request.get_json(silent=True) or {}
                current_settings = auth_service.get_user_settings(user['id'])
                if "failover_provider_sequence" in new_settings:
                    current_settings["failover_provider_sequence"] = new_settings["failover_provider_sequence"]
                    
                auth_service.update_user_settings(user['id'], current_settings)
                return jsonify({"success": True, "settings": current_settings})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/sso/login', methods=['GET'])
    @app.route('/v1/sso/login', methods=['GET'])
    def sso_login():
        from authlib.integrations.flask_client import OAuth
        from synora_server.utils.storage_config import StorageManager
        
        settings = StorageManager.get_instance().get_active_settings()
        sso_enabled = str(settings.value("sso/enable", "false")).lower() == "true"
        if not sso_enabled:
            return jsonify({"error": "Enterprise SSO is disabled."}), 403
            
        client_id = str(settings.value("sso/client_id", ""))
        client_secret = str(settings.value("sso/client_secret", ""))
        discovery_url = str(settings.value("sso/discovery_url", ""))
        
        if not all([client_id, client_secret, discovery_url]):
            return jsonify({"error": "SSO configuration is incomplete."}), 500

        oauth = OAuth(app)
        oauth.register(
            name='enterprise_sso',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=discovery_url,
            client_kwargs={'scope': 'openid email profile'}
        )
        
        from flask import url_for
        redirect_uri = url_for('sso_callback', _external=True)
        return oauth.enterprise_sso.authorize_redirect(redirect_uri)

    @app.route('/api/sso/callback', methods=['GET'])
    @app.route('/v1/sso/callback', methods=['GET'])
    def sso_callback():
        from authlib.integrations.flask_client import OAuth
        from synora_server.utils.storage_config import StorageManager
        
        settings = StorageManager.get_instance().get_active_settings()
        client_id = str(settings.value("sso/client_id", ""))
        client_secret = str(settings.value("sso/client_secret", ""))
        discovery_url = str(settings.value("sso/discovery_url", ""))
        
        oauth = OAuth(app)
        oauth.register(
            name='enterprise_sso',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=discovery_url,
            client_kwargs={'scope': 'openid email profile'}
        )
        
        try:
            token = oauth.enterprise_sso.authorize_access_token()
            userinfo = token.get('userinfo')
        except Exception as e:
            return jsonify({"error": f"SSO handshake failed: {str(e)}"}), 400
            
        if not userinfo:
            return jsonify({"error": "Failed to retrieve user claims from IdP."}), 400
            
        email = userinfo.get('email')
        username = userinfo.get('name') or userinfo.get('preferred_username') or email.split('@')[0]
        
        # Check if user exists in DB
        with db.get_connection() as conn:
            row = conn.execute("SELECT id, username, email, api_key, key_type, status FROM users WHERE email = ?", (email,)).fetchone()
            
        if row:
            user = dict(row)
        else:
            # Auto-provision BYOK tier
            import secrets
            api_key = f"byok_{secrets.token_urlsafe(16)}"
            password = secrets.token_urlsafe(16)
            user_id, err = db.register_user(api_key, username, email, password, "byok")
            if err:
                return jsonify({"error": f"Auto-provisioning failed: {err}"}), 500
            with db.get_connection() as conn:
                row = conn.execute("SELECT id, username, email, api_key, key_type, status FROM users WHERE id = ?", (user_id,)).fetchone()
                user = dict(row)
                
        try:
            from synora_server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            jwt_token = auth_service.generate_token(user)
            user['passport_token'] = jwt_token
            user['token'] = jwt_token
        except Exception as e:
            import logging
            logging.error(f"Failed to generate JWT: {e}")
            user['token'] = user.get('api_key')
            
        from synora_server.utils.logger import AppLogger
        AppLogger.get_instance("synora_saas").siem_audit(
            event_type="sso_login",
            user=user['username'],
            action="enterprise_sso_authentication_success",
            metadata={"email": email, "idp": discovery_url}
        )
            
        return jsonify({
            "success": True,
            "user": user,
            "message": f"SSO Authentication successful. Welcome, {user['username']}."
        })
