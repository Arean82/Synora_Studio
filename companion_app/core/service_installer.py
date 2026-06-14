# companion_app/core/service_installer.py
# Module containing classes: ServiceInstallerController, functions: run_cli_interactive, generate_installer, validate_text.

import os
from pathlib import Path
import logging
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton

logger = logging.getLogger(__name__)

class ServiceInstallerController:
    """
    Decoupled logic for generating Windows (NSSM/PowerShell) or Linux (systemd/bash) Service installation scripts.
    Returns status tuples: (success: bool, message: str)
    """
    def __init__(self, ui_tab=None):
        self.ui_tab = ui_tab
        if self.ui_tab:
            self._wire_gui()

    def _wire_gui(self):
        self.srv_btn = self.ui_tab.findChild(QPushButton, "generateBtn")
        self.srv_combo = self.ui_tab.findChild(QComboBox, "startupTypeCombo")
        self.srv_out = self.ui_tab.findChild(QLabel, "outputLabel")
        
        self.osCombo = self.ui_tab.findChild(QComboBox, "osCombo")
        self.svcName = self.ui_tab.findChild(QLineEdit, "svcName")
        self.svcDesc = self.ui_tab.findChild(QLineEdit, "svcDesc")
        self.linuxUser = self.ui_tab.findChild(QLineEdit, "linuxUser")
        self.linuxGroup = self.ui_tab.findChild(QLineEdit, "linuxGroup")
        self.winUser = self.ui_tab.findChild(QLineEdit, "winUser")
        self.winPass = self.ui_tab.findChild(QLineEdit, "winPass")
        self.restartPolicy = self.ui_tab.findChild(QComboBox, "restartPolicy")
        self.restartDelay = self.ui_tab.findChild(QLineEdit, "restartDelay")
        self.startupDelay = self.ui_tab.findChild(QLineEdit, "startupDelay")
        self.logDir = self.ui_tab.findChild(QLineEdit, "logDir")
        self.envFile = self.ui_tab.findChild(QLineEdit, "envFile")
        from PySide6.QtWidgets import QCheckBox
        self.hardeningCheck = self.ui_tab.findChild(QCheckBox, "hardeningCheck")
        
        def validate_text():
            if self.logDir and self.osCombo.currentIndex() == 1:
                val = self.logDir.text()
                if val.startswith("/") and " " not in val:
                    self.logDir.setStyleSheet("border: 2px solid green;")
                else:
                    self.logDir.setStyleSheet("border: 2px solid red;")
            elif self.logDir:
                self.logDir.setStyleSheet("")
                
            if self.envFile and self.osCombo.currentIndex() == 1:
                val = self.envFile.text()
                if val.startswith("/") and " " not in val:
                    self.envFile.setStyleSheet("border: 2px solid green;")
                else:
                    self.envFile.setStyleSheet("border: 2px solid red;")
            elif self.envFile:
                self.envFile.setStyleSheet("")
                
            if self.linuxUser:
                if " " in self.linuxUser.text():
                    self.linuxUser.setStyleSheet("border: 2px solid red;")
                elif self.linuxUser.text():
                    self.linuxUser.setStyleSheet("border: 2px solid green;")
                    
        if self.osCombo: self.osCombo.currentIndexChanged.connect(validate_text)
        if self.logDir: self.logDir.textChanged.connect(validate_text)
        if self.envFile: self.envFile.textChanged.connect(validate_text)
        if self.linuxUser: self.linuxUser.textChanged.connect(validate_text)
        
        if self.srv_btn:
            self.srv_btn.clicked.connect(self._generate_service)

    def _generate_service(self):
        st_type = "auto" if self.srv_combo.currentIndex() == 0 else "demand"
        os_target = "windows" if self.osCombo.currentIndex() == 0 else "linux"
        name = self.svcName.text().strip() or "llm-chat-backend"
        desc = self.svcDesc.text().strip() or "Background API daemon"
        
        policy = "on-failure"
        restart_sec = "5"
        start_delay = "0"
        log_dir = "logs"
        env_file = ".env"
        hardening = True
        
        if self.restartPolicy: policy = self.restartPolicy.currentText() or "on-failure"
        if self.restartDelay: restart_sec = self.restartDelay.text().strip() or "5"
        if self.startupDelay: start_delay = self.startupDelay.text().strip() or "0"
        if self.logDir: log_dir = self.logDir.text().strip()
        if self.envFile: env_file = self.envFile.text().strip()
        if self.hardeningCheck: hardening = self.hardeningCheck.isChecked()
        
        os_user = "root"
        os_pass = "root"
        
        if os_target == "windows":
            if self.winUser: os_user = self.winUser.text().strip() or "MyAppUser"
            if self.winPass: os_pass = self.winPass.text().strip()
            if not log_dir: log_dir = "logs"
            if not env_file: env_file = ".env"
        else:
            if self.linuxUser: os_user = self.linuxUser.text().strip() or "root"
            if self.linuxGroup: os_pass = self.linuxGroup.text().strip() or "root"
            if not log_dir: log_dir = "/var/log/llm-chat-backend"
            if not env_file: env_file = "/etc/llm-chat-backend/.env"
        
        success, msg = self.generate_installer(os_target, name, desc, st_type, os_user, os_pass, policy, restart_sec, start_delay, log_dir, env_file, hardening)
        self.srv_out.setText(msg)
        if success:
            self.srv_out.setStyleSheet("color: #3fb950; font-weight: bold;")
        else:
            self.srv_out.setStyleSheet("color: #ff7b72; font-weight: bold;")

    @staticmethod
    def run_cli_interactive():
        controller = ServiceInstallerController()
        print("\n--- Background Service Installer ---")
        os_choice = input("Target OS (1=Windows, 2=Linux) [1]: ").strip() or "1"
        os_target = "windows" if os_choice == "1" else "linux"
        
        name = input("Service Name [llm-chat-backend]: ").strip() or "llm-chat-backend"
        desc = input("Description: ").strip() or "Background API daemon"
        
        start_choice = input("Startup (1=Auto, 2=Manual) [1]: ").strip() or "1"
        start_type = "auto" if start_choice == "1" else "demand"
        
        user = "root"
        group = "root"
        policy = "on-failure"
        restart_sec = "5"
        start_delay = "0"
        log_dir = "/var/log/llm-chat-backend"
        env_file = "/etc/llm-chat-backend/.env"
        hardening = True
        
        if os_target == "linux":
            user = input("Linux User [root]: ").strip() or "root"
            group = input("Linux Group [root]: ").strip() or "root"
            policy = input("Restart Policy (on-failure/always/no) [on-failure]: ").strip() or "on-failure"
            restart_sec = input("Restart Delay in sec [5]: ").strip() or "5"
            start_delay = input("Startup Delay in sec [0]: ").strip() or "0"
            log_dir = input("Log Directory [/var/log/llm-chat-backend]: ").strip() or "/var/log/llm-chat-backend"
            env_file = input("Env File [/etc/llm-chat-backend/.env]: ").strip() or "/etc/llm-chat-backend/.env"
            h = input("Apply Security Hardening? (y/n) [y]: ").strip().lower()
            hardening = False if h == 'n' else True
        else:
            user = input("Windows Service User [MyAppUser]: ").strip() or "MyAppUser"
            group = input("Windows User Password: ").strip()
            policy = input("Restart Policy (on-failure/always/no) [on-failure]: ").strip() or "on-failure"
            restart_sec = input("Restart Delay in sec [5]: ").strip() or "5"
            start_delay = input("Startup Delay in sec [0]: ").strip() or "0"
            log_dir = input("Log Directory [logs]: ").strip() or "logs"
            env_file = input("Env File [.env]: ").strip() or ".env"
        
        success, msg = controller.generate_installer(os_target, name, desc, start_type, user, group, policy, restart_sec, start_delay, log_dir, env_file, hardening)
        print(f"\n[{'SUCCESS' if success else 'FAILED'}] {msg}")

    def generate_installer(self, os_target: str, name: str, desc: str, start_type: str, 
                           os_user: str = "root", os_group_or_pass: str = "root", 
                           restart_policy: str = "on-failure", restart_sec: str = "5", startup_delay: str = "0",
                           log_dir: str = "logs", env_file: str = ".env", 
                           hardening: bool = True) -> tuple[bool, str]:
        """
        Generates either install_service.ps1 (Windows NSSM) or a .service file + install_service.sh (Linux)
        """
        try:
            current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
            root_dir = current_dir.parent.parent.parent
            main_exe_path = root_dir / "Synora Studio.exe"
            
            if main_exe_path.exists():
                bin_path = f'"{main_exe_path}"'
                args = '--headless'
            else:
                main_py_path = root_dir / "main.py"
                bin_path = 'python'
                args = f'"{main_py_path}" --headless'

            if os_target == "windows":
                start_nssm = "SERVICE_AUTO_START" if start_type == "auto" else "SERVICE_DEMAND_START"
                win_user = os_user
                win_pass = os_group_or_pass
                
                ps1_content = rf"""<#
.SYNOPSIS
Auto-generated PowerShell Installer for {name}
#>

$ErrorActionPreference = "Stop"

if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {{
    Write-Warning "Please run this script as Administrator."
    Pause
    exit
}}

Write-Host "=== Installing Windows Service: {name} ==="

$AppDir = "{root_dir}"
$LogDir = "{log_dir}"
$EnvFile = "{env_file}"
$SvcUser = "{win_user}"
$SvcPass = "{win_pass}"

$NssmExe = Join-Path $AppDir "nssm.exe"
if (-Not (Test-Path $NssmExe)) {{
    Write-Host "NSSM not found. Downloading the latest secure version..."
    $Url = "https://nssm.cc/release/nssm-2.24.zip"
    $ZipPath = Join-Path $AppDir "nssm.zip"
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath
    Expand-Archive -Path $ZipPath -DestinationPath $AppDir -Force
    Copy-Item -Path (Join-Path $AppDir "nssm-2.24\win64\nssm.exe") -Destination $AppDir
    Remove-Item $ZipPath
    Remove-Item (Join-Path $AppDir "nssm-2.24") -Recurse
    Write-Host "NSSM downloaded successfully."
}}

if (-Not (Get-LocalUser -Name $SvcUser -ErrorAction SilentlyContinue)) {{
    Write-Host "Creating dedicated service user: $SvcUser"
    $SecurePass = ConvertTo-SecureString $SvcPass -AsPlainText -Force
    New-LocalUser -Name $SvcUser -Password $SecurePass -PasswordNeverExpires -Description "Service Account for {name}"
}}

$TempInf = "$env:TEMP\sec.inf"
$TempDb = "$env:TEMP\sec.sdb"
secedit /export /cfg $TempInf /quiet
(Get-Content $TempInf) -replace "^SeServiceLogonRight = .*", "$&,*$SvcUser" | Set-Content $TempInf
secedit /configure /db $TempDb /cfg $TempInf /quiet
Remove-Item $TempInf, $TempDb

if (-Not (Test-Path $LogDir)) {{ New-Item -ItemType Directory -Path $LogDir }}
icacls "$LogDir" /grant "$($SvcUser):(OI)(CI)F" /T /C /Q
icacls "$AppDir" /grant "$($SvcUser):(OI)(CI)F" /T /C /Q

& $NssmExe stop {name}
& $NssmExe remove {name} confirm

& $NssmExe install {name} "{bin_path}" {args}
& $NssmExe set {name} AppDirectory "$AppDir"
& $NssmExe set {name} Description "{desc}"
& $NssmExe set {name} Start $start_nssm

& $NssmExe set {name} AppStdout "$LogDir\service.log"
& $NssmExe set {name} AppStderr "$LogDir\service_error.log"
& $NssmExe set {name} AppStdoutCreationDisposition 4
& $NssmExe set {name} AppStderrCreationDisposition 4

if (Test-Path $EnvFile) {{
    $envLines = Get-Content $EnvFile | Where-Object {{ $_ -match "=" }}
    & $NssmExe set {name} AppEnvironmentExtra $envLines
}}

& $NssmExe set {name} ObjectName ".\$SvcUser" "$SvcPass"

& $NssmExe set {name} AppExit Default Restart
& $NssmExe set {name} AppThrottle {restart_sec}000

Write-Host "Starting {name}..."
& $NssmExe start {name}

Write-Host "✅ Installation complete!"
Pause
"""
                target_file = root_dir / f"install_{name}.ps1"
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(ps1_content)
                return True, f"Successfully generated Windows NSSM installer at:\n{target_file}"
                
            elif os_target == "linux":
                wanted_by = "multi-user.target" if start_type == "auto" else ""
                abs_log_dir = log_dir if log_dir.startswith("/") else f"/var/log/{name}"
                abs_env_file = env_file if env_file.startswith("/") else f"/etc/{name}/.env"
                
                service_content = f"""[Unit]
Description={desc}
After=network-online.target mysql.service postgresql.service
Wants=network-online.target

[Service]
Type=simple
User={os_user}
Group={os_group_or_pass}
WorkingDirectory={root_dir}
EnvironmentFile={abs_env_file}
"""
                if str(startup_delay).strip() and str(startup_delay).strip() != "0":
                    service_content += f"ExecStartPre=/bin/sleep {startup_delay}\n"
                    
                service_content += f"""ExecStart={bin_path.replace('"', '')} {args}
Restart={restart_policy}
RestartSec={restart_sec}
TimeoutStopSec=30
StartLimitBurst=5
StartLimitIntervalSec=10
LimitNOFILE=65536
MemoryMax=2G
"""
                if hardening:
                    service_content += f"""
PrivateTmp=yes
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths={root_dir} {abs_log_dir}
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
"""

                service_content += "\n[Install]\n"
                if wanted_by:
                    service_content += f"WantedBy={wanted_by}\n"
                    
                service_file = root_dir / f"{name}.service"
                with open(service_file, "w", encoding="utf-8") as f:
                    f.write(service_content)
                    
                bash_content = f"""#!/bin/bash
set -e

echo "=== Installing {name} ==="

if ! id "{os_user}" &>/dev/null; then
    echo "Creating dedicated service user: {os_user}"
    useradd -r -s /usr/sbin/nologin {os_user}
fi

mkdir -p {abs_log_dir}
mkdir -p $(dirname {abs_env_file})
touch {abs_env_file}

chown -R {os_user}:{os_group_or_pass} {abs_log_dir}
chown -R {os_user}:{os_group_or_pass} {root_dir}
chown {os_user}:{os_group_or_pass} {abs_env_file}
chmod 600 {abs_env_file}

cp {name}.service /etc/systemd/system/
systemctl daemon-reload

"""
                if start_type == "auto":
                    bash_content += f"systemctl enable --now {name}\n"
                else:
                    bash_content += f"systemctl start {name}\n"
                    
                bash_file = root_dir / f"install_{name}.sh"
                with open(bash_file, "w", encoding="utf-8", newline="\n") as f:
                    f.write(bash_content)
                    
                return True, f"Successfully generated Linux configs at:\n{service_file}\n{bash_file}"
                
            return False, "Unknown Target OS"
            
        except Exception as e:
            logger.exception("Failed to generate service installer script.")
            return False, f"Generation failed: {str(e)}"
