# web/routes/dashboard_routes.py
# Module containing functions: register_dashboard_routes, create_share, view_shared_orbit.

import json
from flask import request, jsonify, render_template

def register_dashboard_routes(app, db):

    @app.route('/api/share', methods=['POST'])
    def create_share():
        user = getattr(request, 'tenant', None)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
            
        data = request.get_json(silent=True) or {}
        conversation_data = data.get("messages")
        
        if not conversation_data:
            return jsonify({"error": "No message data provided."}), 400
            
        share_hash = db.create_share_link(user['id'], json.dumps(conversation_data))
        return jsonify({
            "success": True, 
            "share_url": f"/share/{share_hash}"
        })

    @app.route('/share/<share_hash>', methods=['GET'])
    def view_shared_orbit(share_hash):
        orbit = db.get_shared_orbit(share_hash)
        if not orbit:
            return "Shared Orbit not found or has been deleted.", 404
            
        try:
            orbit['messages'] = json.loads(orbit['conversation_data'])
        except Exception as e: 
            import logging
            logging.error(f"Caught exception: {e}", exc_info=True)
            orbit['messages'] = []
            
        return render_template('share.html', orbit=orbit)

    @app.route('/', methods=['GET'])
    def srv_index():
        return render_template('index.html')
