# synora_saas/core/agent_manager.py
# Module containing classes: AgentManager, functions: get_instance, start_agent, stop_agent.

import subprocess
import os
import sys
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AgentManager:
    """
    Singleton Orchestrator to manage persistent background Hermes Agent processes for tenants.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Maps user_id -> dict of role -> subprocess.Popen object
        self.active_agents: Dict[str, Dict[str, subprocess.Popen]] = {}
        
    def start_agent(self, user_id: str, api_key: str, gateway_url: str, role: str = "Hermes") -> bool:
        """
        Starts a specific Swarm Agent process for a tenant.
        """
        if user_id not in self.active_agents:
            self.active_agents[user_id] = {}
            
        if role in self.active_agents[user_id] and self.active_agents[user_id][role].poll() is None:
            logger.warning(f"{role} Agent for user {user_id} is already running.")
            return True
            
        env = os.environ.copy()
        env["OPENAI_BASE_URL"] = gateway_url
        env["OPENAI_API_KEY"] = api_key
        env["TENANT_USER_ID"] = str(user_id)
        env["AGENT_ROLE"] = role
        
        # Determine the agent entry point (assuming it will be placed in synora_server/logic/agents)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        agent_script = os.path.join(root_dir, "synora_server", "logic", "agents", "hermes_runner.py")
        
        try:
            # We use python executable to launch the agent with piped I/O for real-time streaming
            process = subprocess.Popen(
                [sys.executable, agent_script],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True
            )
            self.active_agents[user_id][role] = process
            logger.info(f"Started {role} Agent for tenant {user_id} with PID {process.pid}")
            
            # Spawn daemon thread to stream stdout directly via Socket.IO to the tenant's browser
            import threading
            from synora_saas.core.app import socketio
            
            def stream_logs(proc, uid):
                # Read line-by-line as the agent thinks and flush to WebSocket
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        socketio.emit('agent_log', {'log': line.strip()}, to=str(uid))
                proc.stdout.close()
                
            threading.Thread(target=stream_logs, args=(process, user_id), daemon=True).start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start agent for tenant {user_id}: {e}")
            return False

    def stop_agent(self, user_id: str, role: str = "Hermes") -> bool:
        """Stops a specific background agent process for a tenant."""
        if user_id in self.active_agents and role in self.active_agents[user_id]:
            process = self.active_agents[user_id][role]
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                del self.active_agents[user_id][role]
                logger.info(f"Stopped {role} Agent for tenant {user_id}")
                return True
        return False
        
    def get_status(self, user_id: str, role: str = "Hermes") -> str:
        """Returns the current process status of the tenant's agent."""
        if user_id in self.active_agents and role in self.active_agents[user_id]:
            process = self.active_agents[user_id][role]
            if process.poll() is None:
                return "RUNNING"
            else:
                return "STOPPED"
        return "NOT_STARTED"
