# Universal Admin Credentials Resetter (`/admin_reset`)

The Admin Reset Utility is a highly destructive, last-resort recovery tool for the Synora ecosystem. 

Because Synora utilizes strictly isolated SQLite/Turso tenant databases and advanced `Argon2id` password hashing, it is impossible to recover a lost password. This module exists to forcefully wipe and regenerate the root administrative account.

## 🛑 DANGER ZONE

**Running this script will:**
1. Connect directly to the underlying `tenant_db.sqlite`.
2. Delete the existing root admin account.
3. Generate a new cryptographic salt and password hash.
4. Insert a fresh root admin account with default credentials.

**Any custom configurations, BYOK (Bring Your Own Key) settings, or usage telemetry associated with the old admin account WILL BE LOST FOREVER.**

## 🚀 Execution Guide

Only run this if you are completely locked out of the Web Portal SaaS dashboard.

**Step 1:** Ensure the API Server and Web Portal are completely shut down (to avoid SQLite locking conflicts).

**Step 2:** Navigate to this directory and execute the reset script:
```bash
cd admin_reset
python reset_admin.py
```

**Step 3:** The terminal will output the newly generated, temporary root password. Copy it securely.

**Step 4:** Restart the API Server and Web Portal, log in with the new credentials, and immediately change your password in the dashboard.
