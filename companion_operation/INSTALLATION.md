# Companion Operation

The Companion Operation is a standalone utility designed to perform administrative and data migration tasks that require the main Synora Studio application to be fully shut down (to release active locks on the SQLite `saas_tenants.db`).

## Execution

Ensure that all other components (Web, Desktop, Server) are completely shut down before running this utility.

To run the companion tool manually:
```bash
python companion_operation.py
```

*Note: The Desktop Client can also launch this utility automatically via the Settings menu by safely shutting itself down first.*
