# Administrator Reset Tool

The Admin Reset tool is a dedicated utility used to purge corrupt data, reset system configurations, or clear locked state in the SaaS platform without requiring direct database intervention.

## Execution

Ensure that the main components (Web, Server) are shut down before performing a deep reset to avoid SQLite `database is locked` errors.

To run the reset utility:
```bash
python admin_reset.py
```
