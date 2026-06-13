# web/routes/admin_routes.py
# Module containing functions: register_admin_routes, sync_admin_prompts, admin_gen_params.

import os
import time
import json
from flask import request, jsonify
from server.utils.path_utils import get_resource_path
from server.utils.security_utils import admin_required

def register_admin_routes(app, db):

    @app.route('/api/admin/system_prompts', methods=['GET', 'POST'])
    @app.route('/v1/admin/system_prompts', methods=['GET', 'POST'])
    @app.route('/v2/admin/system_prompts', methods=['GET', 'POST'])
    def sync_admin_prompts():
        prompts_file = get_resource_path("resources/user_prompts.json")
        
        if request.method == 'GET':
            try:
                if os.path.exists(prompts_file):
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return jsonify({"success": True, "data": data})
                else:
                    return jsonify({"success": True, "data": []})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
                
        if request.method == 'POST':
            try:
                payload = request.get_json(silent=True) or []
                with open(prompts_file, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=4)
                return jsonify({"success": True, "message": "Synced to Desktop Globally"})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/gen_params', methods=['GET', 'POST'])
    @app.route('/v1/admin/gen_params', methods=['GET', 'POST'])
    @app.route('/v2/admin/gen_params', methods=['GET', 'POST'])
    @admin_required(audit_message="Admin parameters access")
    def admin_gen_params():
        config_file = get_resource_path("resources/config.json")
        if request.method == 'GET':
            try:
                if os.path.exists(config_file):
                    with open(config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return jsonify({"success": True, "data": data})
                return jsonify({"success": True, "data": {}})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
                
        if request.method == 'POST':
            try:
                payload = request.get_json(silent=True) or {}
                if os.path.exists(config_file):
                    with open(config_file, 'r', encoding='utf-8') as f:
                        current = json.load(f)
                else:
                    current = {}
                current.update(payload)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(current, f, indent=4)
                return jsonify({"success": True, "message": "Synced to Desktop Globally"})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/local_api', methods=['GET', 'POST'])
    @app.route('/v1/admin/local_api', methods=['GET', 'POST'])
    @app.route('/v2/admin/local_api', methods=['GET', 'POST'])
    @admin_required(audit_message="Admin local API access")
    def admin_local_api():
        from server.utils.path_utils import get_app_settings
        settings = get_app_settings()
        
        if request.method == 'GET':
            enabled = str(settings.value("api_enabled", "true")).lower() == "true"
            key = settings.value("local_api_auth_key", "")
            return jsonify({"success": True, "enabled": enabled, "key": key})
            
        if request.method == 'POST':
            payload = request.get_json(silent=True) or {}
            action = payload.get("action")
            
            if action == "toggle":
                current_enabled = str(settings.value("api_enabled", "true")).lower() == "true"
                new_enabled = not current_enabled
                settings.setValue("api_enabled", "true" if new_enabled else "false")
                
                instance = getattr(app, "saas_server_instance", None)
                if instance:
                    instance.api_manager_action.emit("restart" if new_enabled else "stop")
                return jsonify({"success": True, "enabled": new_enabled})
                
            elif action == "regen":
                import uuid
                new_key = f"llm-local-auth-{uuid.uuid4().hex[:10]}"
                settings.setValue("local_api_auth_key", new_key)
                
                instance = getattr(app, "saas_server_instance", None)
                if instance:
                    instance.api_manager_action.emit("restart")
                return jsonify({"success": True, "key": new_key})
                
            return jsonify({"success": False, "error": "Unknown action"}), 400

    @app.route('/api/admin/saas_config', methods=['GET', 'POST'])
    @app.route('/v1/admin/saas_config', methods=['GET', 'POST'])
    @app.route('/v2/admin/saas_config', methods=['GET', 'POST'])
    @admin_required(audit_message="Admin SaaS config access")
    def admin_saas_config():
        try:
            from web.core.config_manager import SaaSConfigManager
            saas_cfg = SaaSConfigManager()
            
            if request.method == 'GET':
                data = {
                    "smtp_enabled": saas_cfg.get_bool("SMTP_RELAY", "enabled", False),
                    "smtp_host": saas_cfg.get_str("SMTP_RELAY", "host", "smtp.gmail.com"),
                    "smtp_port": saas_cfg.get_int("SMTP_RELAY", "port", 587),
                    "smtp_user": saas_cfg.get_str("SMTP_RELAY", "user", ""),
                    "smtp_password": saas_cfg.get_str("SMTP_RELAY", "password", "")
                }
                return jsonify({"success": True, "data": data})
                
            if request.method == 'POST':
                payload = request.get_json(silent=True) or {}
                if "smtp_enabled" in payload: saas_cfg.set_val("SMTP_RELAY", "enabled", payload["smtp_enabled"])
                if "smtp_host" in payload: saas_cfg.set_val("SMTP_RELAY", "host", payload["smtp_host"])
                if "smtp_port" in payload: saas_cfg.set_val("SMTP_RELAY", "port", int(payload["smtp_port"]))
                if "smtp_user" in payload: saas_cfg.set_val("SMTP_RELAY", "user", payload["smtp_user"])
                if "smtp_password" in payload: saas_cfg.set_val("SMTP_RELAY", "password", payload["smtp_password"])
                saas_cfg.save()
                return jsonify({"success": True, "message": "SaaS Config Synced"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/models', methods=['POST'])
    @app.route('/v1/admin/models', methods=['POST'])
    @app.route('/v2/admin/models', methods=['POST'])
    @admin_required(audit_message="Admin models access")
    def admin_models():
        try:
            from server.logic.model_io import load_all_models, save_models
            data = request.get_json(silent=True) or {}
            if not data.get("id"):
                return jsonify({"success": False, "error": "Model ID is required."}), 400
                
            models = load_all_models()
            existing_idx = next((i for i, m in enumerate(models) if m.get("id") == data["id"]), None)
            
            if existing_idx is not None:
                models[existing_idx].update(data)
            else:
                models.append(data)
                
            save_models(models)
            return jsonify({"success": True, "message": "Model synced to Desktop."})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/v1/system/providers', methods=['GET', 'POST'])
    @app.route('/v2/system/providers', methods=['GET', 'POST'])
    def list_system_providers():
        try:
            from server.logic.model_io import load_provider_metadata
            from server.utils.path_utils import get_app_settings
            
            if request.method == 'POST':
                user = getattr(request, 'tenant', None)
                try:
                    from server.logic.services import ServiceRegistry
                    security_svc = ServiceRegistry.get("security")
                    if not security_svc.check_permission(user, "admin"):
                        security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Add system provider access denied", "FAILED")
                        return jsonify({"error": "Forbidden. Operator access only."}), 403
                    security_svc.log_audit(user.get('id'), request.path, "Add system provider access granted", "SUCCESS")
                except Exception as e: 
                    import logging
                    logging.error(f"Caught exception: {e}", exc_info=True)
                    if not user or user.get('key_type') != 'admin_funded':
                        return jsonify({"error": "Forbidden. Operator access only."}), 403
                    
                data = request.get_json(silent=True)
                if not data or 'sdk' not in data or 'ecosystem' not in data or 'url' not in data:
                    return jsonify({"error": "Missing required fields."}), 400
                    
                settings = get_app_settings()
                custom_raw = settings.value("custom_providers", "[]")
                try:
                    custom_providers = json.loads(custom_raw)
                except:
                    custom_providers = []
                    
                custom_providers.append({
                    "sdk": data["sdk"],
                    "ecosystem": data["ecosystem"],
                    "url": data["url"]
                })
                settings.setValue("custom_providers", json.dumps(custom_providers))
                return jsonify({"success": True})
            
            metadata = load_provider_metadata()
            raw_providers = metadata.get("providers", [])
            
            base_providers = []
            for p in raw_providers:
                base_providers.append({
                    "id": p.get("id"),
                    "sdk": p.get("sdk", "openai"),
                    "ecosystem": p.get("display_name", p.get("id")),
                    "default_url": p.get("default_url", "")
                })
                
            settings = get_app_settings()
            custom_raw = settings.value("custom_providers", "[]")
            try:
                custom_providers = json.loads(custom_raw)
            except:
                custom_providers = []
                
            formatted_custom = []
            for c in custom_providers:
                eco_key = c['ecosystem'].lower().replace(' ', '_')
                formatted_custom.append({
                    "id": f"{c['sdk']}_{eco_key}", 
                    "sdk": c['sdk'],
                    "ecosystem": c['ecosystem'],
                    "default_url": c['url']
                })
                
            return jsonify({"base": base_providers, "custom": formatted_custom})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/admin/users', methods=['GET'])
    @app.route('/v1/admin/users', methods=['GET'])
    @app.route('/v2/admin/users', methods=['GET'])
    def admin_list_users():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin list users denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin list users granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        users = db.get_all_tenants()
        for u in users:
            settings = db.get_user_settings(u['id'])
            u['requests_per_minute_limit'] = settings.get('requests_per_minute_limit', 60 if u['username'] != 'admin' else 0)
        return jsonify({"success": True, "users": users})
        
    @app.route('/api/admin/stats', methods=['GET'])
    @app.route('/v1/admin/stats', methods=['GET'])
    @app.route('/v2/admin/stats', methods=['GET'])
    def admin_stats():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin stats access denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin stats access granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        stats = db.get_global_usage()
        return jsonify({"success": True, "stats": stats})

    @app.route('/api/admin/telemetry', methods=['GET'])
    @app.route('/v1/admin/telemetry', methods=['GET'])
    @app.route('/v2/admin/telemetry', methods=['GET'])
    def admin_telemetry():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin telemetry access denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin telemetry access granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        try:
            from server.logic.services import ServiceRegistry
            from server.logic.queue.job_queue import JobQueueEngine
            
            telemetry_service = ServiceRegistry.get("telemetry")
            metrics = telemetry_service.get_realtime_metrics()
            
            metrics["health"] = telemetry_service.run_health_checks()
            
            circuit_breaker = ServiceRegistry.get("circuit_breaker")
            metrics["circuit_breaker_state"] = circuit_breaker.state if circuit_breaker else "CLOSED"
            
            try:
                queue_engine = JobQueueEngine()
                status = queue_engine.get_queue_status()
                active_list = status.get("processing_jobs", []) + status.get("queued_jobs", [])
                
                serialized_jobs = []
                for row, job in enumerate(active_list):
                    serialized_jobs.append({
                        "name": f"WorkerThread-{row+1}",
                        "job_id": str(job.get("job_id", "")),
                        "task_type": f"Ingest: {job.get('task_type', '')}",
                        "status": str(job.get("status", "")).upper()
                    })
                metrics["active_jobs"] = serialized_jobs
            except Exception as q_ex:
                metrics["active_jobs"] = []
                print(f"[Telemetry API] Error gathering queue status: {q_ex}")
                
            return jsonify({"success": True, "metrics": metrics})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/tenants/<int:tenant_id>/rate-limit', methods=['POST'])
    @app.route('/v1/admin/tenants/<int:tenant_id>/rate-limit', methods=['POST'])
    @app.route('/v2/admin/tenants/<int:tenant_id>/rate-limit', methods=['POST'])
    def admin_set_tenant_rate_limit(tenant_id):
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin set tenant rate limit denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin set tenant rate limit granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        payload = request.get_json(silent=True) or {}
        rpm = payload.get("requests_per_minute_limit")
        if rpm is None:
            return jsonify({"error": "Missing requests_per_minute_limit"}), 400
            
        try:
            rpm = int(rpm)
            if rpm < 0:
                return jsonify({"error": "Rate limit must be non-negative"}), 400
        except ValueError:
            return jsonify({"error": "Invalid rate limit value"}), 400
            
        try:
            from server.logic.services import ServiceRegistry
            auth_service = ServiceRegistry.get("auth")
            current_settings = auth_service.get_user_settings(tenant_id)
            current_settings["requests_per_minute_limit"] = rpm
            auth_service.update_user_settings(tenant_id, current_settings)
            return jsonify({"success": True, "message": f"Tenant rate limit updated to {rpm} RPM"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/dlq', methods=['GET'])
    @app.route('/v1/admin/dlq', methods=['GET'])
    @app.route('/v2/admin/dlq', methods=['GET'])
    def admin_get_dlq():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin get DLQ access denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin get DLQ access granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        try:
            from server.logic.queue.job_queue import JobQueueEngine
            queue_engine = JobQueueEngine()
            entries = queue_engine.get_dlq_entries()
            return jsonify({"success": True, "dlq": entries})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/dlq/retry', methods=['POST'])
    @app.route('/v1/admin/dlq/retry', methods=['POST'])
    @app.route('/v2/admin/dlq/retry', methods=['POST'])
    def admin_retry_dlq_job():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin retry DLQ job denied", "FAILED")
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin retry DLQ job granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            if not user or user.get('key_type') != 'admin_funded':
                return jsonify({"error": "Forbidden. Operator access only."}), 403
            
        payload = request.get_json(silent=True) or {}
        job_id = payload.get("job_id")
        if not job_id:
            return jsonify({"error": "Missing job_id"}), 400
            
        try:
            from server.logic.queue.job_queue import JobQueueEngine
            queue_engine = JobQueueEngine()
            new_job_id = queue_engine.retry_dlq_job(job_id)
            return jsonify({"success": True, "new_job_id": new_job_id, "message": f"Job successfully enqueued as {new_job_id}."})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/extensions/save', methods=['POST'])
    @app.route('/v1/admin/extensions/save', methods=['POST'])
    @app.route('/v2/admin/extensions/save', methods=['POST'])
    def save_extension_meta():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin save extension meta denied", "FAILED")
                return jsonify({"success": False, "error": "Unauthorized"}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin save extension meta granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            is_admin = user and user.get('key_type') == 'admin_funded'
            if not is_admin:
                return jsonify({"success": False, "error": "Unauthorized"}), 403

        data = request.get_json(silent=True) or {}
        filename = data.get("filename")
        if not filename:
            return jsonify({"success": False, "error": "Missing filename"}), 400

        config_path = get_resource_path(os.path.join("extension", "extensions_config.json"))
        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except Exception as e: 
                pass

        if filename not in config_data:
            config_data[filename] = {}

        config_data[filename]["is_visible"] = bool(data.get("is_visible", False))
        config_data[filename]["description"] = data.get("description", "")
        config_data[filename]["name"] = data.get("name", filename.split('-')[0].title())

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/admin/extensions/generate-desc', methods=['POST'])
    @app.route('/v1/admin/extensions/generate-desc', methods=['POST'])
    @app.route('/v2/admin/extensions/generate-desc', methods=['POST'])
    def generate_extension_desc():
        user = getattr(request, 'tenant', None)
        try:
            from server.logic.services import ServiceRegistry
            security_svc = ServiceRegistry.get("security")
            if not security_svc.check_permission(user, "admin"):
                security_svc.log_audit(user.get('id', 'anonymous'), request.path, "Admin generate extension desc denied", "FAILED")
                return jsonify({"success": False, "error": "Unauthorized"}), 403
            security_svc.log_audit(user.get('id'), request.path, "Admin generate extension desc granted", "SUCCESS")
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            is_admin = user and user.get('key_type') == 'admin_funded'
            if not is_admin:
                return jsonify({"success": False, "error": "Unauthorized"}), 403

        data = request.get_json(silent=True) or {}
        filename = data.get("filename")
        platform = data.get("platform", "vscode")
        if not filename:
            return jsonify({"success": False, "error": "Missing filename"}), 400

        prompt = (
            f"Write a highly professional, beautifully formatted, concise README-style Markdown description "
            f"for an IDE Extension plugin. The file name is '{filename}' and it is for the '{platform}' ecosystem.\n\n"
            f"Provide a brief overview of features (like inline autocomplete, model parameters editing, and workspace syncing), "
            f"step-by-step instructions on how to install it, and connection instructions "
            f"(explaining how it connects to the local Universal API server on Port 5000).\n\n"
            f"Keep it under 300 words. Do not use generic placeholders. Focus on premium glassmorphic UI synergy and security."
        )

        try:
            from server.logic.llm_client import LLMClient
            llm_client = LLMClient()
            from server.utils.path_utils import get_app_settings
            active_p = get_app_settings().value("active_provider_id", "nvidia")
            import keyring
            api_key = keyring.get_password("LLMChatApp", f"api_key_{active_p}") or keyring.get_password("LLMChatApp", "api_key")
            base_url = get_app_settings().value(f"url_{active_p}") or get_app_settings().value("base_url", "https://integrate.api.nvidia.com/v1")
            
            if not api_key:
                return jsonify({"success": False, "error": "Active provider API key is not configured in desktop vault."}), 400

            llm_client.set_api_key(api_key)
            llm_client.set_base_url(base_url)
            
            from server.logic.model_io import load_all_models
            model_id = get_app_settings().value("current_model_id")
            if not model_id:
                active_models = [m for m in load_all_models() if m.get('provider', 'nvidia') == active_p and m.get('free', True)]
                model_id = active_models[0]["id"] if active_models else "meta/llama-3.1-8b-instruct"
            llm_client.set_model(model_id)

            full_response = llm_client._run_completion_internal("You are an expert technical writer.", prompt, 1024, 0.3)
            return jsonify({"success": True, "description": full_response.strip()})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
