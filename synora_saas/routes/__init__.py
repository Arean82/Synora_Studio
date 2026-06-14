# synora_saas/routes/__init__.py
# Utility script or configuration module.

from .auth_routes import register_auth_routes
from .admin_routes import register_admin_routes
from .api_routes import register_api_routes
from .dashboard_routes import register_dashboard_routes
from .system_routes import register_system_routes

__all__ = [
    'register_auth_routes',
    'register_admin_routes',
    'register_api_routes',
    'register_dashboard_routes',
    'register_system_routes'
]
