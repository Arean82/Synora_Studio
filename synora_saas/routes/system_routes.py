# synora_saas/routes/system_routes.py
# Module containing functions: register_system_routes, srv_health, system_shutdown.

import os
import time
import json
from flask import request, jsonify, send_from_directory
from synora_server.utils.path_utils import get_resource_path

def register_system_routes(app):

    @app.route('/health', methods=['GET'])
    @app.route('/v1/health', methods=['GET'])
    @app.route('/v2/health', methods=['GET'])
    def srv_health():
        return jsonify({
            "status": "online", 
            "service": "Multi-Tenant Cloud Node", 
            "timestamp": int(time.time())
        })

    @app.route('/v1/system/shutdown', methods=['POST'])
    def system_shutdown():
        if request.remote_addr not in ['127.0.0.1', '::1', 'localhost']:
            return jsonify({"success": False, "error": "Unauthorized"}), 403
            
        import signal
        def shutdown():
            time.sleep(0.5)
            os.kill(os.getpid(), signal.SIGINT)
            
        import threading
        threading.Thread(target=shutdown, daemon=True).start()
        return jsonify({"success": True, "message": "Flushing databases and shutting down."})

    @app.route('/api/documents/list', methods=['GET'])
    @app.route('/v1/documents/list', methods=['GET'])
    @app.route('/v2/documents/list', methods=['GET'])
    def list_documents():
        user = getattr(request, 'tenant', None)
        is_admin = user and user.get('key_type') == 'admin_funded'
        docs = ["README_ADMIN.md", "README_USER.md", "API_SPEC.md", "IDE_INTEGRATION.md", "SECURITY.md"] if is_admin else ["README_USER.md", "API_SPEC.md"]
        return jsonify({"success": True, "documents": docs})

    @app.route('/api/documents/content/<doc_name>', methods=['GET'])
    @app.route('/v1/documents/content/<doc_name>', methods=['GET'])
    @app.route('/v2/documents/content/<doc_name>', methods=['GET'])
    def get_document_content(doc_name):
        user = getattr(request, 'tenant', None)
        is_admin = user and user.get('key_type') == 'admin_funded'
        admin_docs = ["README_ADMIN.md", "IDE_INTEGRATION.md", "SECURITY.md"]
        user_docs = ["README_USER.md", "API_SPEC.md"]
        if doc_name not in admin_docs and doc_name not in user_docs:
            return jsonify({"success": False, "error": "Not Found"}), 404
        if not is_admin and doc_name in admin_docs:
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        try:
            doc_path = get_resource_path(os.path.join("synora_saas", "saas_docs", doc_name))
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"success": True, "content": content})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/extensions', methods=['GET'])
    @app.route('/v1/extensions', methods=['GET'])
    @app.route('/v2/extensions', methods=['GET'])
    def list_extensions():
        user = getattr(request, 'tenant', None)
        is_admin = user and user.get('key_type') == 'admin_funded'

        ext_dir = get_resource_path("extension")
        config_path = get_resource_path(os.path.join("extension", "extensions_config.json"))

        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except Exception as e:
                pass

        discovered = []
        if os.path.exists(ext_dir):
            for file in os.listdir(ext_dir):
                if file.endswith('.vsix') or file.endswith('.zip'):
                    file_path = os.path.join(ext_dir, file)
                    size_bytes = os.path.getsize(file_path)
                    
                    if size_bytes < 1024 * 1024:
                        size_str = f"{size_bytes / 1024:.1f} KB"
                    else:
                        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

                    platform = "vscode" if file.endswith('.vsix') else "jetbrains"
                    
                    import re
                    ver_match = re.search(r'-(\d+\.\d+\.\d+)\.', file)
                    version = ver_match.group(1) if ver_match else "1.0.0"

                    config_item = config_data.get(file, {})
                    is_visible = config_item.get("is_visible", False)
                    description = config_item.get("description", "No description available.")
                    name = config_item.get("name", file.split('-')[0].replace('_', ' ').title())

                    item_meta = {
                        "filename": file,
                        "name": name,
                        "version": version,
                        "platform": platform,
                        "is_visible": is_visible,
                        "description": description,
                        "file_size": size_str,
                        "updated_at": time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(file_path)))
                    }

                    if is_admin or is_visible:
                        discovered.append(item_meta)

        return jsonify({"success": True, "extensions": discovered})

    @app.route('/api/extensions/download/<filename>', methods=['GET'])
    @app.route('/v1/extensions/download/<filename>', methods=['GET'])
    @app.route('/v2/extensions/download/<filename>', methods=['GET'])
    def download_extension(filename):
        filename = os.path.basename(filename)
        ext_dir = get_resource_path("extension")
        file_path = os.path.join(ext_dir, filename)

        if not os.path.exists(file_path):
            return jsonify({"success": False, "error": "Extension file not found"}), 404

        user = getattr(request, 'tenant', None)
        is_admin = user and user.get('key_type') == 'admin_funded'

        if not is_admin:
            config_path = get_resource_path(os.path.join("extension", "extensions_config.json"))
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                        if not config_data.get(filename, {}).get("is_visible", False):
                            return jsonify({"success": False, "error": "Unauthorized Access"}), 403
                except Exception as e: 
                    return jsonify({"success": False, "error": "Unauthorized Access"}), 403
            else:
                return jsonify({"success": False, "error": "Unauthorized Access"}), 403

        return send_from_directory(ext_dir, filename, as_attachment=True)

    @app.route('/app_icon.ico')
    def app_icon():
        from flask import send_file
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'app_icon.ico'))
        if os.path.exists(icon_path):
            return send_file(icon_path, mimetype='image/x-icon')
        return "", 404

    @app.route('/favicon.ico', methods=['GET'])
    def srv_favicon():
        from synora_server.utils.path_utils import get_resource_path
        icon_dir = get_resource_path("resources")
        return send_from_directory(icon_dir, "app_icon.ico")
