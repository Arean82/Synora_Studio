# Web Portal Installation Guide (Beginner Friendly)

This guide will walk you through setting up the **Synora SaaS Web Portal**. 
Because Synora Studio is modular, the web portal operates completely independently but **it requires the API Server to be running on port 5000** to function. Ensure you have completed the `server/INSTALLATION.md` steps first.

Choose your operating system below and follow the exact commands in your terminal.

---

## 🐧 Linux / Ubuntu (Production & Dev)

**Step 1: Open Terminal**
Navigate to the root directory of the repository (where the main `requirements.txt` file is located).

**Step 2: Create a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
```

**Step 3: Activate the Virtual Environment**
```bash
source venv/bin/activate
```

**Step 4: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Start the Web Portal**
Navigate into the `web` directory and run the portal:
```bash
cd web
python run_web.py
```

---

## 🪟 Windows (Development)

**Step 1: Open PowerShell**
Navigate to the root directory of the repository.

**Step 2: Create a Virtual Environment**
```powershell
python -m venv venv
```

**Step 3: Activate the Virtual Environment**
```powershell
.\venv\Scripts\activate
```

**Step 4: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Start the Web Portal**
```powershell
python web\run_web.py
```

---

## 🌐 Accessing the Portal

Once the server says `Running on http://0.0.0.0:8080/`, you can open your web browser and navigate to:

👉 **http://localhost:8080**

### First Time Setup:
1. Since there are no user accounts yet, you will be prompted to create the first Tenant/Admin account.
2. The web portal will securely hash your password and store it in your dedicated SQLite/Turso tenant database.
3. Once logged in, the Web Portal will connect to the API Server running in the background to handle all LLM and RAG capabilities.
