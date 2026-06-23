# synora_server/logic/api_server.py
# Module containing classes: APIServer, functions: setup_security, setup_routes, stream_response.

import threading

from flask import Flask, request, jsonify, Response, stream_with_context
from threading import Thread
import time
import json
from collections import OrderedDict

class APIServer:
    def __init__(self, llm_client, send_message_callback, stream_callback=None):
        self.app = Flask(__name__)
        self.llm_client = llm_client
        self.send_message_callback = send_message_callback
        self.stream_callback = stream_callback
        self.port = 5000
        self.server = None
        self.running = False
        self.running = False
        self.conversation_history = OrderedDict()  # Store history per session with LRU capability
        self._history_lock = threading.Lock()  # Lock for thread-safe history access
        self.MAX_HISTORY_SESSIONS = 100  # Safeguard to prevent memory leaks
        try:
            from flasgger import Swagger
            self.swagger = Swagger(self.app, template={
                "info": {
                    "title": "Synora Studio Headless API",
                    "description": "Enterprise-grade AI chat ecosystem and RAG platform.",
                    "version": "1.0.0"
                }
            })
        except ImportError:
            self.swagger = None
        self.setup_routes()
        self.setup_security()
    
    def setup_security(self):
        from synora_server.utils.path_utils import get_app_settings
        import uuid
        import os
        
        settings = get_app_settings()
        
        # Determine API key: Priority to Environment Variable (for Docker/Production), fallback to QSettings
        env_api_key = os.environ.get("SYNORA_API_KEY")
        if env_api_key:
            api_key = env_api_key
        else:
            api_key = settings.value("local_api_auth_key", "")
            if not api_key:
                api_key = f"llm-local-auth-{uuid.uuid4().hex[:10]}"
                settings.setValue("local_api_auth_key", api_key)
                settings.sync()
            
        @self.app.before_request
        def verify_auth():
            # Exempt health endpoint if needed, or lock everything down
            if request.path == '/health':
                return None
            
            auth_header = request.headers.get('Authorization')
            
            # Fetch the dynamic key. Again, prioritize env var in case it was injected later.
            current_key = os.environ.get("SYNORA_API_KEY") or settings.value("local_api_auth_key", "")
            expected = f"Bearer {current_key}"
            
            if not auth_header or auth_header != expected:
                return jsonify({"error": "Unauthorized. Invalid local API key."}), 401

    def setup_routes(self):
        @self.app.route('/v1/models', methods=['GET'])
        def list_models():
            """
            List available models
            ---
            tags:
              - Models
            responses:
              200:
                description: A list of available AI models
            """
            return jsonify({
                "data": [{
                    "id": self.llm_client.current_model or "unknown",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "llm-chat-app"
                }]
            })
        
        @self.app.route('/v1/chat/completions', methods=['POST'])
        def chat_completion():
            """
            Chat Completions endpoint
            ---
            tags:
              - Chat
            parameters:
              - in: body
                name: body
                required: true
                schema:
                  type: object
                  properties:
                    messages:
                      type: array
                      items:
                        type: object
                        properties:
                          role:
                            type: string
                          content:
                            type: string
                    stream:
                      type: boolean
                    temperature:
                      type: number
                    max_tokens:
                      type: integer
                    session_id:
                      type: string
            responses:
              200:
                description: Successful response (can be stream or JSON)
            """
            data = request.get_json(silent=True) or {}
            messages = data.get('messages', [])
            stream = data.get('stream', False)
            temperature = data.get('temperature', 0.7)
            max_tokens = data.get('max_tokens', 4096)
            session_id = data.get('session_id', 'default')
            
            # Extract messages
            user_message = ""
            system_message = ""
            for msg in messages:
                if msg.get('role') == 'system':
                    system_message = msg.get('content', '')
                elif msg.get('role') == 'user':
                    user_message = msg.get('content', '')
            
            if not user_message:
                return jsonify({"error": "No user message found"}), 400
            
            # Store conversation history (THREAD-SAFE)
            with self._history_lock:
                if session_id not in self.conversation_history:
                    # Check and enforce max history cap
                    if len(self.conversation_history) >= self.MAX_HISTORY_SESSIONS:
                        self.conversation_history.popitem(last=False) # Discard the oldest accessed session
                    self.conversation_history[session_id] = []
                
                # Update user message and refresh access order
                self.conversation_history[session_id].append({"role": "user", "content": user_message})
                self.conversation_history.move_to_end(session_id)
            
            if stream:
                def generate():
                    full_response = ""
                    for chunk in self.stream_response(user_message, system_message, temperature, max_tokens, messages_list=messages):
                        full_response += chunk
                        yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk}}]})}\n\n"
                    
                    # Final touch: move updated session to most recent position
                    with self._history_lock:
                        if session_id in self.conversation_history:
                            self.conversation_history[session_id].append({"role": "assistant", "content": full_response})
                            self.conversation_history.move_to_end(session_id)
                    yield "data: [DONE]\n\n"
                
                return Response(generate(), mimetype='text/event-stream')
            else:
                # Call the app's send function with parameters
                response = self.send_message_callback(
                    user_message, 
                    messages_list=messages,
                    system_message=system_message,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Store assistant response in history (THREAD-SAFE)
                with self._history_lock:
                    if session_id in self.conversation_history:
                        self.conversation_history[session_id].append({"role": "assistant", "content": response})
                        self.conversation_history.move_to_end(session_id)
                
                return jsonify({
                    "id": "chatcmpl-" + str(int(time.time())),
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": self.llm_client.current_model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0
                    }
                })
        
        @self.app.route('/v1/chat/history/<session_id>', methods=['DELETE'])
        def clear_history(session_id):
            """
            Clear Conversation History
            ---
            tags:
              - Chat
            parameters:
              - in: path
                name: session_id
                required: true
                type: string
            responses:
              200:
                description: Status of the deletion operation
            """
            with self._history_lock:
                if session_id in self.conversation_history:
                    del self.conversation_history[session_id]
            return jsonify({"status": "cleared"})
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """
            Health Check
            ---
            tags:
              - System
            responses:
              200:
                description: Current status and active model
            """
            return jsonify({"status": "running", "model": self.llm_client.current_model})
            
        @self.app.route('/v1/system/shutdown', methods=['POST'])
        def system_shutdown():
            """
            Graceful Shutdown
            ---
            tags:
              - System
            responses:
              200:
                description: Initiates server shutdown
              403:
                description: Unauthorized access (must be localhost)
            """
            if request.remote_addr not in ['127.0.0.1', '::1', 'localhost']:
                return jsonify({"error": "Unauthorized"}), 403
            
            import threading
            def delayed_stop():
                import time
                time.sleep(0.5)
                self.stop()
            threading.Thread(target=delayed_stop, daemon=True).start()
            return jsonify({"success": True, "message": "API Server shutting down."})
    
    def stream_response(self, user_message, system_message="", temperature=0.7, max_tokens=4096, messages_list=None):
        """Generator for streaming responses"""
        if self.stream_callback:
            for chunk in self.stream_callback(user_message, system_message, temperature, max_tokens, messages_list=messages_list):
                yield chunk
        else:
            # Fallback to non-streaming
            response = self.send_message_callback(
                user_message, 
                messages_list=messages_list, 
                system_message=system_message, 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            yield response
    
    def start(self):
        if self.running:
            return True, "Already running"
        
        # Check if port 5000 is available
        import socket
        import sys
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', 5000))
            except OSError:
                msg = "Port 5000 is already in use."
                if sys.platform == 'darwin':
                    msg += " (On macOS, disable 'AirPlay Receiver' in System Settings > General > AirPlay & Handoff)"
                elif sys.platform == 'win32':
                    msg += " (Check if another instance or a web service is using this port)"
                return False, msg
        
        try:
            from werkzeug.serving import make_server
            self.server = make_server('localhost', 5000, self.app, threaded=True)
            
            def run():
                print(f"API Server starting on http://localhost:5000")
                self.server.serve_forever()
            
            self.server_thread = Thread(target=run, daemon=True)
            self.server_thread.start()
            self.running = True
            return True, "API Server Started. API is running on http://localhost:5000"
        except Exception as e:
            return False, f"Server Error: {str(e)}"
    
    def stop(self):
        if self.server:
            print("Shutting down API Server...")
            self.server.shutdown()
            self.server = None
        self.running = False
        return True, "API Server Stopped."
    
    def get_status(self):
        return {"running": self.running, "port": self.port, "model": self.llm_client.current_model}
