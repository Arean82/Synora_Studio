# synora_saas/routes/api_routes.py
# Module containing functions: register_api_routes, user_settings, agent_status.

import os
import time
import json
from flask import request, jsonify, Response, stream_with_context
from synora_server.logic.llm_client import LLMClient

def register_api_routes(app, db, get_provider_base_url):

    @app.route('/api/user/settings', methods=['GET', 'POST'])
    @app.route('/v1/user/settings', methods=['GET', 'POST'])
    @app.route('/v2/user/settings', methods=['GET', 'POST'])
    def user_settings():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        if request.method == 'GET':
            settings = db.get_user_settings(user['id'])
            return jsonify({"success": True, "data": settings})
            
        if request.method == 'POST':
            payload = request.get_json(silent=True) or {}
            success = db.update_user_settings(user['id'], payload)
            if success:
                return jsonify({"success": True, "message": "Settings updated"})
            return jsonify({"success": False, "error": "Failed to update settings"}), 500

    @app.route('/api/agent/status', methods=['GET'])
    @app.route('/v1/agent/status', methods=['GET'])
    def agent_status():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        from synora_server.logic.agents.agent_manager import AgentManager
        mgr = AgentManager.get_instance()
        status = mgr.get_status(user['id'])
        return jsonify({"success": True, "status": status})

    @app.route('/api/agent/start', methods=['POST'])
    @app.route('/v1/agent/start', methods=['POST'])
    def agent_start():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        from synora_server.logic.agents.agent_manager import AgentManager
        mgr = AgentManager.get_instance()
        gateway_url = f"http://localhost:{os.getenv('PORT', 5000)}/v1"
        success = mgr.start_agent(user['id'], user['api_key'], gateway_url)
        if success:
            db.update_agent_instance(user['id'], "Hermes", "running")
            return jsonify({"success": True, "status": "RUNNING"})
        return jsonify({"success": False, "error": "Failed to start agent"}), 500

    @app.route('/api/agent/stop', methods=['POST'])
    @app.route('/v1/agent/stop', methods=['POST'])
    def agent_stop():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        from synora_server.logic.agents.agent_manager import AgentManager
        mgr = AgentManager.get_instance()
        success = mgr.stop_agent(user['id'])
        if success:
            db.update_agent_instance(user['id'], "Hermes", "stopped")
            return jsonify({"success": True, "status": "STOPPED"})
        return jsonify({"success": False, "error": "Failed to stop agent"}), 500

    @app.route('/api/agent/skills', methods=['GET'])
    @app.route('/v1/agent/skills', methods=['GET'])
    def agent_skills_list():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        skills = db.get_agent_skills(user['id'])
        skills_list = [dict(row) for row in skills]
        return jsonify({"success": True, "skills": skills_list})

    @app.route('/api/agent/skills/add', methods=['POST'])
    @app.route('/v1/agent/skills/add', methods=['POST'])
    def agent_skills_add():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"success": False, "error": "Unauthorized action scope."}), 401
            
        data = request.get_json() or {}
        skill_name = data.get("skill_name", "").strip()
        skill_code = data.get("skill_code", "").strip()
        
        if not skill_name or not skill_code:
            return jsonify({"success": False, "error": "Missing skill name or code"}), 400
            
        try:
            db.add_agent_skill(user['id'], skill_name, skill_code)
            return jsonify({"success": True, "message": "Skill added successfully"})
        except Exception as e:
            from synora_server.utils.logger import AppLogger
            AppLogger.get_instance("synora_saas").error(f"Failed to add skill: {e}")
            return jsonify({"success": False, "error": "Database error adding skill"}), 500

    @app.route('/v1/models', methods=['GET'])
    @app.route('/v2/models', methods=['GET'])
    def list_saas_models():
        try:
            from synora_server.logic.model_io import load_all_models, load_provider_metadata
            from synora_server.utils.model_config import does_model_support_tools
            all_models = load_all_models()
            
            is_admin = request.tenant['username'] == 'admin' if hasattr(request, 'tenant') else False
            tenant_creds = db.get_tenant_credentials(request.tenant['id']) if hasattr(request, 'tenant') and not is_admin else {}
            
            import keyring
            model_data = []
            for m in all_models:
                prov = m.get('provider', 'nvidia').lower()
                has_key = False
                
                if is_admin:
                    metadata = load_provider_metadata()
                    base_providers = {p.get("id"): p for p in metadata.get("providers", [])}
                    
                    def normalize(p): return str(p).lower().replace(" ", "").replace("_", "").replace("-", "")
                    
                    p_id = normalize(prov)
                    mapped_id = p_id
                    for base_id, base_p in base_providers.items():
                        if normalize(base_p.get("display_name", "")) == p_id or normalize(base_id) == p_id:
                            mapped_id = base_id
                            break
                            
                    if mapped_id in base_providers:
                        if keyring.get_password("LLMChatApp", f"api_key_{mapped_id}"):
                            has_key = True
                        elif mapped_id == "nvidia" and keyring.get_password("LLMChatApp", "api_key"):
                            has_key = True
                    
                    if not has_key:
                        from synora_server.utils.path_utils import get_app_settings
                        custom = json.loads(get_app_settings().value("custom_providers", "[]"))
                        for cp in custom:
                            if normalize(cp['ecosystem']) == p_id:
                                eco_key = cp['ecosystem'].lower().replace(' ', '_')
                                if keyring.get_password("LLMChatApp", f"api_key_{cp['sdk']}_{eco_key}"):
                                    has_key = True
                                    break
                else:
                    has_key = prov in tenant_creds and bool(tenant_creds[prov])
                    
                if prov in ['local', 'ollama', 'lmstudio']:
                    has_key = True
                    
                if has_key:
                    m_id = m.get("id", "")
                    m_desc = m.get("description", "").lower()
                    is_vision = "vision" in m_id.lower() or "-vl" in m_id.lower() or "vision" in m_desc or "multimodal" in m_desc
                    
                    model_data.append({
                        "id": m_id,
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": m.get("provider", "llm-chat-app"),
                        "name": m.get("name", m_id),
                        "description": m.get("description", ""),
                        "free": m.get("free", True),
                        "developer": m.get("developer", ""),
                        "capabilities": {
                            "chat": m.get('type', 'chat') == 'chat',
                            "tools": does_model_support_tools(m_id),
                            "vision": is_vision
                        }
                    })
                
            return jsonify({"data": model_data})
        except Exception as e:
            return jsonify({"data": []})

    @app.route('/api/memory/list', methods=['GET'])
    def memory_list():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
            
        workspace = db.get_user_workspace(user['id'])
        v_path = workspace.get('vector_path')
        
        collections = []
        if v_path and v_path.exists():
            for item in v_path.iterdir():
                if item.is_dir():
                    collections.append({
                        "name": item.name,
                        "created": os.path.getctime(str(item))
                    })
                    
        return jsonify({"success": True, "collections": collections})

    @app.route('/v1/chat/completions', methods=['POST'])
    @app.route('/v2/chat/completions', methods=['POST'])
    def proxy_chat_completion():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
            
        data = request.get_json(silent=True) or {}
        is_arena_request = data.get("arena_mode", False) or data.get("is_duel", False)
        
        if is_arena_request and user['key_type'] == 'admin_funded':
            return jsonify({
                "error": "Forbidden. Parallel Model Arena is locked for Admin-Funded accounts.",
                "message": "Admin accounts are restricted to standard chat models to preserve compute balances."
            }), 403

        try:
            from synora_server.logic.services import ServiceRegistry
            cog_router = ServiceRegistry.get("cognitive_router")
            if not cog_router.check_billing_quota(user['id']):
                return jsonify({
                    "error": "Quota Exhausted",
                    "message": "Your allocated token quota has been exhausted. Please contact your system administrator."
                }), 402
        except Exception as quota_ex:
            pass

        user_msg = ""
        system_msg = ""
        messages = data.get("messages", [])
        for m in messages:
            if m.get("role") == "system": system_msg = m.get("content", "")
            elif m.get("role") == "user": user_msg = m.get("content", "")

        stream = data.get("stream", False)
        web_search_enabled = data.get("web_search", False)
        
        task = data.get("task", "chat")
        model_id = data.get("model", "meta/llama-3.1-8b-instruct")
        try:
            from synora_server.logic.services import ServiceRegistry
            cog_router = ServiceRegistry.get("cognitive_router")
            model_id = cog_router.route_model(user['id'], task, model_id)
        except Exception as route_ex:
            pass

        if user_msg and not web_search_enabled:
            try:
                from synora_server.logic.services import ServiceRegistry
                cache_svc = ServiceRegistry.get("cache")
                
                cached_response = db.get_semantic_cache_hit(user_msg, user['id'])
                if cached_response:
                    if cache_svc: cache_svc.hits += 1
                    if stream:
                        def generate_cache_stream():
                            yield f"data: {json.dumps({'choices': [{'delta': {'content': cached_response}}]})}\n\n"
                            yield "data: [DONE]\n\n"
                        return Response(stream_with_context(generate_cache_stream()), mimetype="text/event-stream")
                    else:
                        return jsonify({
                            "id": f"chatcmpl-cache-{int(time.time())}",
                            "object": "chat.completion",
                            "created": int(time.time()),
                            "model": model_id,
                            "choices": [{"message": {"role": "assistant", "content": cached_response}}],
                            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                        })
                else:
                    if cache_svc: cache_svc.misses += 1
            except Exception as e:
                pass
        
        if web_search_enabled and user_msg:
            try:
                from synora_server.logic.tool_manager import ToolManager
                search_res = ToolManager.execute_web_search(user_msg, limit=3)
                if search_res and "⚠️" not in search_res:
                    injection = f"\n\n[SYSTEM TOOL CONTEXT: The user requested a real-time web search. Results:\n{search_res}\nUse these results to formulate your answer.]"
                    system_msg += injection
                    has_sys = False
                    for m in messages:
                        if m.get("role") == "system":
                            m["content"] = system_msg
                            has_sys = True
                    if not has_sys:
                        messages.insert(0, {"role": "system", "content": system_msg})
            except Exception as e:
                pass
        
        api_passport = user['api_key']
        llm_client = LLMClient()
        llm_client.set_model(model_id)
        provider = llm_client.get_current_provider()
        
        api_execution_key = api_passport
        if user.get('key_type') == 'admin_funded':
            try:
                import keyring
                funded_key = keyring.get_password("LLMChatApp", f"api_key_{provider}")
                if not funded_key and provider == "nvidia":
                    funded_key = keyring.get_password("LLMChatApp", "api_key")
                
                if not funded_key:
                    from synora_server.logic.tenant.config_manager import SaaSConfigManager
                    cfg = SaaSConfigManager()
                    funded_key = cfg.get_str("GLOBAL_KEYS", f"{provider}_api_key", "").strip()
                    
                if funded_key: api_execution_key = funded_key
                else: api_execution_key = None

            except Exception as cred_ex:
                pass
        
        if not api_execution_key:
            return jsonify({
                "error": "Missing Credentials", 
                "message": f"API key for '{provider}' is not configured in the Admin Desktop Console. Please add it via Settings -> Credential Manager."
            }), 400

        if provider == "google":
            llm_client.set_google_api_key(api_execution_key)
        else:
            base_url = get_provider_base_url(provider)
            llm_client.set_base_url(base_url)
            llm_client.set_api_key(api_execution_key)

        prompt_chars = sum(len(m.get("content", "")) for m in messages)
        approx_prompt_tokens = int(prompt_chars / 4)

        final_url = getattr(llm_client, "base_url", "")
        if final_url and user.get('username') != 'admin':
            if any(host in final_url.lower() for host in ['localhost', '127.0.0.1', '0.0.0.0']):
                return jsonify({
                    "error": "Forbidden", 
                    "message": "Local infrastructure models (Ollama/LM Studio) are restricted to the Super Admin."
                }), 403

        try:
            from synora_server.logic.services import ServiceRegistry
            circuit_breaker = ServiceRegistry.get("circuit_breaker")
        except KeyError:
            circuit_breaker = None

        def run_completion(*args, **kwargs):
            if provider == "google":
                from google.genai import types
                gemini_method = getattr(llm_client.google_client.models, "generate_content")
                resp = gemini_method(
                    model=llm_client.current_model,
                    contents=[m.get("content") for m in messages if m.get("role") != "system"],
                    config=types.GenerateContentConfig(
                        system_instruction=system_msg or None,
                        safety_settings=[
                            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE)
                        ]
                    )
                )
                return getattr(resp, "text")
            else:
                if user_msg:
                    try:
                        moderation_fn = getattr(llm_client.client, "moderations")
                        moderation_create = getattr(moderation_fn, "create")
                        moderation_create(input=user_msg)
                    except Exception as e: 
                        pass

                from openai import RateLimitError, APIError
                try:
                    completions_fn = getattr(llm_client.client.chat, "completions")
                    create_fn = getattr(completions_fn, "create")
                    resp = create_fn(
                        model=llm_client.current_model,
                        messages=messages,
                        max_tokens=4096,
                        user=str(user.get('id', 'default_user'))
                    )
                except RateLimitError as e: raise e
                except APIError as e: raise e
                except Exception as e: raise e

                refusal = getattr(resp.choices[0].message, "refusal", None)
                if refusal: raise ValueError(f"Request refused by model: {refusal}")
                return getattr(resp.choices[0].message, "content")

        try:
            if stream:
                if circuit_breaker and circuit_breaker.is_enabled():
                    current_cb_state = circuit_breaker.check_state()
                    if current_cb_state == "OPEN":
                        text = circuit_breaker._execute_failover(user['id'], llm_client, run_completion, system_msg, user_msg, 4096, 0.7)
                        def generate_failover_stream():
                            yield f"data: {json.dumps({'choices': [{'delta': {'content': text}}]})}\n\n"
                            yield "data: [DONE]\n\n"
                        return Response(stream_with_context(generate_failover_stream()), mimetype="text/event-stream")

                try:
                    if provider == "google":
                        from google.genai import types
                        gemini_stream_method = getattr(llm_client.google_client.models, "generate_content_stream")
                        stream_resp = gemini_stream_method(
                            model=llm_client.current_model,
                            contents=[m.get("content") for m in messages if m.get("role") != "system"],
                            config=types.GenerateContentConfig(
                                system_instruction=system_msg or None,
                                safety_settings=[
                                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
                                    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE)
                                ]
                            )
                        )
                    else:
                        if user_msg:
                            try:
                                moderation_fn = getattr(llm_client.client, "moderations")
                                moderation_create = getattr(moderation_fn, "create")
                                moderation_create(input=user_msg)
                            except Exception as e: 
                                pass

                        completions_fn = getattr(llm_client.client.chat, "completions")
                        create_fn = getattr(completions_fn, "create")
                        stream_resp = create_fn(
                            model=llm_client.current_model,
                            messages=messages,
                            stream=True,
                            max_tokens=4096,
                            user=str(user.get('id', 'default_user'))
                        )
                except Exception as stream_init_error:
                    if circuit_breaker and circuit_breaker.is_enabled():
                        circuit_breaker.record_failure()
                        text = circuit_breaker._execute_failover(user['id'], llm_client, run_completion, system_msg, user_msg, 4096, 0.7)
                        def generate_failover_stream():
                            yield f"data: {json.dumps({'choices': [{'delta': {'content': text}}]})}\n\n"
                            yield "data: [DONE]\n\n"
                        return Response(stream_with_context(generate_failover_stream()), mimetype="text/event-stream")
                    raise stream_init_error

                def generate_stream():
                    response_text = ""
                    try:
                        if provider == "google":
                            for chk in stream_resp:
                                if chk.text:
                                    response_text += chk.text
                                    yield f"data: {json.dumps({'choices': [{'delta': {'content': chk.text}}]})}\n\n"
                        else:
                            for chunk in stream_resp:
                                if chunk.choices and chunk.choices[0].delta.content:
                                    text = chunk.choices[0].delta.content
                                    response_text += text
                                    yield f"data: {json.dumps({'choices': [{'delta': {'content': text}}]})}\n\n"
                        
                        if circuit_breaker:
                            circuit_breaker.record_success()

                        approx_comp_tokens = int(len(response_text) / 4)
                        db.record_usage(user['id'], approx_prompt_tokens, approx_comp_tokens)
                        
                        if user_msg and response_text and not web_search_enabled:
                            try: db.set_semantic_cache_hit(user_msg, user['id'], response_text)
                            except Exception as e: pass
                                
                        yield "data: [DONE]\n\n"
                        
                    except Exception as e:
                        if circuit_breaker: circuit_breaker.record_failure()
                        err_msg = str(e).replace('"', '\\"')
                        yield f"data: {json.dumps({'error': err_msg})}\n\n"
                        yield "data: [DONE]\n\n"

                return Response(stream_with_context(generate_stream()), mimetype="text/event-stream")
                
            else:
                if circuit_breaker and circuit_breaker.is_enabled():
                    text = circuit_breaker.execute(user['id'], llm_client, run_completion, system_msg, user_msg, 4096, 0.7)
                else:
                    text = run_completion()
                
                approx_comp_tokens = int(len(text) / 4)
                db.record_usage(user['id'], approx_prompt_tokens, approx_comp_tokens)
                
                if user_msg and text and not web_search_enabled:
                    try: db.set_semantic_cache_hit(user_msg, user['id'], text)
                    except Exception as e: pass
                
                return jsonify({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": model_id,
                    "choices": [{"message": {"role": "assistant", "content": text}}],
                    "usage": {
                        "prompt_tokens": approx_prompt_tokens,
                        "completion_tokens": approx_comp_tokens,
                        "total_tokens": approx_prompt_tokens + approx_comp_tokens
                    }
                })

        except Exception as e:
            return jsonify({"error": "Generation Engine Exception", "message": str(e)}), 500
