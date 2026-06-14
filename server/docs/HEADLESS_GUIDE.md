# Server Daemonization Guide (Headless)

Because the API Server is a pure backend multiplexer, it is designed to run silently in the background of your host OS without attaching to a visible terminal.

This guide explains how to configure the server to launch automatically on boot using `systemd` (Linux) or Windows Services.

## 🐧 Linux `systemd` Deployment

The recommended way to deploy the API server on Ubuntu/Debian is via a `systemd` service.

**Step 1:** Create a service file at `/etc/systemd/system/synora-server.service`
```ini
[Unit]
Description=Synora Studio API Server
After=network.target

[Service]
User=synora_user
WorkingDirectory=/path/to/Synora_Studio/server
Environment="PATH=/path/to/Synora_Studio/venv/bin"
ExecStart=/path/to/Synora_Studio/venv/bin/python run_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Step 2:** Reload the daemon and enable the service.
```bash
sudo systemctl daemon-reload
sudo systemctl enable synora-server
sudo systemctl start synora-server
```

**Step 3:** View the live server logs.
```bash
sudo journalctl -u synora-server -f
```

## 🪟 Windows Background Deployment

To run the server silently on Windows without a Command Prompt window appearing, you can use `pythonw.exe` instead of `python.exe`.

1. Press `Win + R` and type `shell:startup`.
2. Create a new shortcut in this folder.
3. Set the target to your virtual environment's `pythonw.exe`, passing the `run_server.py` script as an argument.
```
C:\path\to\Synora_Studio\venv\Scripts\pythonw.exe C:\path\to\Synora_Studio\server\run_server.py
```
This ensures the server API is instantly available to your Desktop GUI or Web Portal as soon as you log into Windows.
