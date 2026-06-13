# Companion Operation & Service Daemon Installer

The Companion Operation is a dual-mode administrative utility that facilitates platform migration, local data relocations, database backups, network/web configuration, and system service daemon generation.

## Features
- **Database Relocation**: Autonomously migrates all schemas and data from local bootstrap environments (Turso/libSQL SQLite) up to production enterprise clusters (PostgreSQL).
- **Network/Web Configuration**: Programmatically update host binding and ports for the SaaS Web Portal via GUI or CLI.
- **Global SSH Piggybacking**: Seamlessly reads SSH Tunnel configurations stored in the Desktop App (`config.ini`) to securely tunnel Database Relocations and Backend Administration commands over encrypted, firewalled connections.
- **Automated Service Generation (Daemon Installer)**:
  - Generates native background daemon configurations.
  - **Windows (NSSM)**: Generates a PowerShell script (`install_<name>.ps1`) that automatically downloads NSSM, configures execution, locks down permissions, and installs the API as a Windows Service.
  - **Linux (systemd)**: Generates a `.service` file and automated bash script (`install_<name>.sh`) that configures systemd, sets up dedicated service users, and configures security hardening (such as `PrivateTmp`, `ProtectHome`, and restricted capabilities).
- **Backend Administration**:
  - **Demo User Injection**: Injects a pre-verified `demo@grid.net` user safely into the active database without polluting SaaS architecture. (Piggybacks SSH tunnel if hosted).
  - **Danger Zone / Platform Reset**: Safely executes a strict destructive reset of all tenants, wiping all multi-tenant footprints while preserving the master admin. (Piggybacks SSH tunnel if hosted).
- **Intelligent Headless & Dual-Mode Execution**:
  - **Intelligent Headless CLI Mode**: Interactive terminal wizard or scriptable actions (e.g. `--action=backup`). Bypasses GUI dependencies entirely.
  - **GUI Mode**: PySide6 step-by-step wizard panel for local desktop environments.

## Local Configuration & Packaging Files
To support decoupled modular compilation, this directory contains its own self-contained packaging files:
- **`companion_operation.spec`**: PyInstaller spec file specific to packaging the Companion Operation tool.
- **`build.py`**: Local Python build script executing PyInstaller commands targeting `companion_operation.spec`. (Global orchestrator is in `scripts/build.py`).
- **`file_version_info.txt`**: OS-level metadata defining the executable's version, copyrights, and descriptions.
- **`installer_script.iss`**: Local Inno Setup configuration to package the compiled Companion Operation tool.

## Execution

### CLI Mode:
```bash
python companion_operation.py --headless
```

### CLI Scripting Examples:
```bash
# Inject demo user
python companion_operation.py --headless --action create-user --demo-user

# Danger Zone: Reset Web Platform (using Desktop App SSH config)
python companion_operation.py --headless --action danger-zone --desktop-config-path "C:\Path\To\Desktop\App"
```

### PyInstaller Spec
To compile the standalone binary `Companion_Operation` using PyInstaller:
```bash
pyinstaller companion_operation.spec
```
This ensures private operator tools are compiled separate from the main desktop user bundle.
