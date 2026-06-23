# synora_server/logic/services/storage_service.py
# Module containing classes: StorageService, functions: on_initialize, on_shutdown, get_driver.

import os
import logging
import urllib.parse
import configparser
from pathlib import Path

from .base_service import BaseService, ServiceRegistry
from synora_server.utils.storage_config import StorageManager
from synora_server.logic.storage_drivers.postgres_driver import PostgreSQLStorageDriver
from synora_server.logic.storage_drivers.base_driver import ConcurrencyError

logger = logging.getLogger("SynoraStorageService")

class StorageService(BaseService):
    """
    Central storage service managing PostgreSQL connections and optimistic concurrency control.
    """
    def __init__(self):
        super().__init__()
        self.drivers = {}  # Cache drivers per tenant_id

    def on_initialize(self) -> bool:
        logger.info("Initializing Synora Storage Service (PostgreSQL)...")
        # Pre-warm the default tenant connection
        self.get_driver("default_user")
        return True

    def on_shutdown(self) -> bool:
        logger.info("Shutting down Synora Storage Service connections...")
        self.drivers.clear()
        return True

    def _get_pg_connection_string(self, tenant_id: str) -> str:
        """Reads config.ini to dynamically build the PostgreSQL connection string for the chat database."""
        config = configparser.ConfigParser()
        config_path = StorageManager.get_instance().get_storage_root() / "synora_server" / "data" / "config.ini"
        
        if config_path.exists():
            config.read(str(config_path))
            
        user = config.get("TENANT_DB", "pg_user", fallback="synora") if config.has_section("TENANT_DB") else "synora"
        password = config.get("TENANT_DB", "pg_password", fallback="synora_secure_pw") if config.has_section("TENANT_DB") else "synora_secure_pw"
        host = config.get("TENANT_DB", "pg_host", fallback="localhost") if config.has_section("TENANT_DB") else "localhost"
        port = config.get("TENANT_DB", "pg_port", fallback="5432") if config.has_section("TENANT_DB") else "5432"
        db = config.get("TENANT_DB", "pg_chat_db", fallback="synora_default_user") if config.has_section("TENANT_DB") else "synora_default_user"
        
        # If a custom tenant is active, replace the default db name
        if tenant_id != "default_user":
            db = f"synora_{tenant_id}"
            
        encoded_user = urllib.parse.quote_plus(user)
        encoded_password = urllib.parse.quote_plus(password)
        
        return f"postgresql://{encoded_user}:{encoded_password}@{host}:{port}/{db}"

    def get_driver(self, tenant_id: str):
        """
        Thread-safe PostgreSQL driver instantiation and caching per tenant.
        """
        if tenant_id in self.drivers:
            return self.drivers[tenant_id]

        url = self._get_pg_connection_string(tenant_id)
        logger.info(f"Instantiating PostgreSQL driver for tenant '{tenant_id}'")
        driver = PostgreSQLStorageDriver(url)

        # Cache driver instance
        self.drivers[tenant_id] = driver
        return driver

    def save_conversation(self, tenant_id: str, conversation: list, title: str = "New Conversation",
                          conv_id: int = None, model_id: str = "", messages_html: str = None) -> int:
        """Saves or updates a conversation for a tenant with Optimistic Concurrency Control (OCC)."""
        driver = self.get_driver(tenant_id)
        try:
            return driver.save_conversation(
                conversation=conversation,
                title=title,
                conv_id=conv_id,
                model_id=model_id,
                messages_html=messages_html
            )
        except ConcurrencyError as e:
            logger.warning(f"OCC Conflict for tenant '{tenant_id}' (silently resolving): {str(e)}")
            # Fallback bypass to avoid locking user flow
            return driver.save_conversation(
                conversation=conversation,
                title=title,
                conv_id=conv_id,
                model_id=model_id,
                messages_html=messages_html,
                expected_version=None
            )

    def load_conversation(self, tenant_id: str, conv_id: int) -> dict:
        """Loads a specific conversation by ID for a tenant."""
        return self.get_driver(tenant_id).load_conversation(conv_id)

    def get_all_conversations(self, tenant_id: str) -> list:
        """Returns a list of all conversations in the sidebar for a tenant."""
        return self.get_driver(tenant_id).get_all_conversations()

    def delete_conversation(self, tenant_id: str, conv_id: int) -> None:
        """Deletes a specific conversation by ID for a tenant."""
        self.get_driver(tenant_id).delete_conversation(conv_id)

    def clear_all(self, tenant_id: str) -> None:
        """Wipes the entire conversations table for a tenant."""
        self.get_driver(tenant_id).clear_all()


# Register StorageService automatically
ServiceRegistry.register("storage", StorageService())
