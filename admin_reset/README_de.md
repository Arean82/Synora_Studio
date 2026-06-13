# Universal Admin Credentials Resetter (v9.0)

Mit diesem Tool können Serveradministratoren die Master-Administrator-Anmeldeinformationen in allen Umgebungen sicher zurücksetzen.

## Funktionen
- **Dual-Mode-Ausführung**:
  - **GUI-Modus**: Erzeugt einen hochpräzisen PySide6-Assistentendialog für lokale Desktop-Umgebungen.
  - **CLI/Headless-Modus**: Umgeht GUI-Abhängigkeiten vollständig mit „--headless“ oder „--cli“ und eignet sich somit perfekt für Remote-SSH-Terminals, Automatisierungsskripte und Cron-Jobs.
- **Dynamische Passwortoptionen**:
  - „--random-password“: Erzeugt ein sicheres, zufälliges 12-stelliges alphanumerisches Passwort.
  - „--custom-password „your_password““: Legt eine bestimmte, benutzerdefinierte Passwortzeichenfolge fest.
  – Standardmäßig ist das Passwort „admin“, wenn keine Option angegeben ist.
- **Automatische Treibererkennung**: Liest automatisch Verbindungsinformationen und löst Treiberparameter aus „saas/config.ini“ oder der Umgebung auf.

## Lokale Konfigurations- und Verpackungsdateien
Um die entkoppelte modulare Kompilierung zu unterstützen, enthält dieses Verzeichnis seine eigenen, eigenständigen Paketdateien:
- **`reset_admin.spec`**: PyInstaller-Spezifikationsdatei speziell für das Packen des Admin-Reset-Tools.
- **`build.py`**: Lokales Python-Build-Skript, das PyInstaller-Befehle ausführt, die auf „reset_admin.spec“ abzielen. (Der globale Orchestrator befindet sich in „scripts/build.py“).
- **`file_version_info.txt`**: Metadaten auf Betriebssystemebene, die die Version der ausführbaren Datei (v9.0.0.0), Urheberrechte und Beschreibungen definieren.
- **`installer_script.iss`**: Lokale Inno-Setup-Konfiguration zum Packen des kompilierten Admin-Reset-Tools.

## Ausführung

### CLI/Headless-Modus:
„Bash
python reset_admin.py --headless
„

### PyInstaller-Spezifikation
So kompilieren Sie die eigenständige Binärdatei „Admin_Reset“ mit PyInstaller:
„Bash
pyinstaller reset_admin.spec
„
Dadurch wird die Funktion zum Zurücksetzen des Passworts von öffentlichen Client-Distributionen isoliert, wodurch die Sicherheit der Verwaltungsschlüssel gewährleistet bleibt.