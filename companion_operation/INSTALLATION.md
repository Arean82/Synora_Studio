# Companion Operation Toolkit Installation

The **Companion Operation Toolkit** is a highly restricted, privileged administrative tool used by DevOps engineers and System Administrators to manage the Synora ecosystem. 

Because it hooks into the core database and active backend services, **you must ensure the API Server is already configured and running** before using the toolkit.

---

## 🛠️ Installation & Setup (Linux/Windows)

The companion toolkit runs as a standalone Python utility.

**Step 1: Open your Terminal / PowerShell**
Navigate to the root directory of the repository.

**Step 2: Activate your Virtual Environment**
Ensure you are using the same virtual environment that you created for the server.
- **Linux:** `source venv/bin/activate`
- **Windows:** `.\venv\Scripts\activate`

**Step 3: Run the Toolkit**
Navigate to the companion module and start the interactive CLI:
```bash
cd companion_operation
python companion_operation.py
```

## ⚠️ Warning

The Companion Toolkit operates with **Global Administrator Privileges**. Operations performed here (like Database Wipes, Demo User Injections, and automated Backup/Restore hooks) are irreversible. 

Ensure you have a recent backup before executing any migrations.
