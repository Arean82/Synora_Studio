# Companion Operation & Service Daemon Installer (v9.0)

Die Companion Operation ist ein Dual-Mode-Verwaltungsdienstprogramm, das Plattformmigration, lokale Datenverschiebungen, Datenbanksicherungen, Netzwerk-/Webkonfiguration und Systemdienst-Daemon-Generierung erleichtert.

## Funktionen
- **Datenbankverlagerung**: Migriert automatisch alle Schemata und Daten von lokalen Bootstrap-Umgebungen (Turso/libSQL SQLite) bis zu Produktions-Unternehmensclustern (PostgreSQL).
- **Netzwerk-/Webkonfiguration**: Hostbindung und Ports für das SaaS-Webportal programmgesteuert über GUI oder CLI aktualisieren.
- **Automatisierte Dienstgenerierung (Daemon Installer)**:
  – Erzeugt native Hintergrund-Daemon-Konfigurationen.
  - **Windows (NSSM)**: Erstellt ein PowerShell-Skript („install_<name>.ps1“), das NSSM automatisch herunterlädt, die Ausführung konfiguriert, Berechtigungen sperrt und die API als Windows-Dienst installiert.
  - **Linux (systemd)**: Erzeugt eine „.service“-Datei und ein automatisiertes Bash-Skript („install_<name>.sh“), das systemd konfiguriert, dedizierte Dienstbenutzer einrichtet und Sicherheitshärtung konfiguriert (z. B. „PrivateTmp“, „ProtectHome“ und eingeschränkte Funktionen).
- **Dual-Mode-Ausführung**:
  - **GUI-Modus**: Schritt-für-Schritt-Assistent für PySide6.
  - **CLI-Modus**: Interaktiver Terminal-Assistent oder skriptfähige Aktionen (z. B. „--action=backup“).

## Lokale Konfigurations- und Verpackungsdateien
Um die entkoppelte modulare Kompilierung zu unterstützen, enthält dieses Verzeichnis seine eigenen, eigenständigen Paketdateien:
- **`companion_operation.spec`**: PyInstaller-Spezifikationsdatei speziell für das Packen des Companion Operation-Tools.
- **`build.py`**: Lokales Python-Build-Skript, das PyInstaller-Befehle ausführt, die auf „companion_operation.spec“ abzielen. (Der globale Orchestrator befindet sich in „scripts/build.py“).
- **`file_version_info.txt`**: Metadaten auf Betriebssystemebene, die die Version der ausführbaren Datei (v9.0.0.0), Urheberrechte und Beschreibungen definieren.
- **`installer_script.iss`**: Lokale Inno-Setup-Konfiguration zum Packen des kompilierten Companion Operation-Tools.

## Ausführung

### CLI-Modus:
„Bash
Python Companion_operation.py --headless
„

### PyInstaller-Spezifikation
So kompilieren Sie die eigenständige Binärdatei „Companion_Operation“ mit PyInstaller:
„Bash
pyinstaller Companion_operation.spec
„
Dadurch wird sichergestellt, dass private Betreibertools getrennt vom Haupt-Desktop-Benutzerpaket zusammengestellt werden.