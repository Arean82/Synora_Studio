# Compilation Manual: Building Executables

Because Synora Studio is broken into independent modules, you cannot compile the entire repository into a single `.exe` file. Instead, you must compile the Server and the Desktop Client separately using `PyInstaller`.

## ⚙️ Prerequisites

Before compiling, ensure you have PyInstaller installed in your virtual environment:
```bash
pip install pyinstaller
```

---

## 🛠️ Compiling the API Server (Headless Daemon)

The Server must be compiled as a standalone background executable.

**Step 1:** Navigate to the server module.
```bash
cd server
```

**Step 2:** Run the PyInstaller command. We use `--noupx` to avoid corrupting ONNX model libraries, and `--hidden-import` to ensure all AI SDKs are bundled.
```bash
pyinstaller --name "Synora_Server" --onedir --console \
  --hidden-import=google.generativeai \
  --hidden-import=openai \
  --hidden-import=anthropic \
  server.py
```

**Step 3:** Your compiled backend will be located in `/server/dist/Synora_Server/`.

---

## 🖥️ Compiling the Desktop GUI

The Desktop Client must be compiled as a windowed application.

**Step 1:** Navigate to the desktop module.
```bash
cd desktop
```

**Step 2:** Run PyInstaller. We use `--windowed` (or `-w`) to prevent a command prompt from appearing behind the PyQt6 GUI.
```bash
pyinstaller --name "Synora_Desktop" --onedir --windowed \
  --icon=resources/app_icon.ico \
  main.py
```

**Step 3:** Your compiled GUI will be located in `/desktop/dist/Synora_Desktop/`.

---

## 📦 Deployment Strategy

When distributing the software to your end-users, you must package both compiled folders into your installer (e.g., using InnoSetup or NSIS). Your installer should configure the OS to silently launch `Synora_Server.exe` as a background service on startup, while placing a shortcut to `Synora_Desktop.exe` on the user's desktop.
