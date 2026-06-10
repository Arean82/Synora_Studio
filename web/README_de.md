# Web-SaaS-Portal und Multi-Tenant-Gateway (v9.0)

Dieses Verzeichnis hostet das Webanwendungsportal, das Datenbank-Routing-Switchboard, dynamische Tenant-Sandboxing-Engines und SaaS-Client-Verwaltungsschnittstellen.

## Verzeichnisstruktur
- **`app.py`**: Der zentrale Flask-Anwendungscontroller, der Routen, JWT-Authentifizierungen, Mandantenanmeldungen, Sitzungsabläufe und REST-Endpunkte verwaltet.
- **`run_web.py`**: Standard-Skript-Runner, der die „App“-Instanz importiert und die Serverschleife startet.
- **`core/`**: SaaS-Kernhilfsmodule (z. B. „launcher.py“, „agent_manager.py“, „config_manager.py“, „tenant_db.py“).
- **`tenant_drivers/`**: Middleware, die Schemaisolationen und Cloud-Datenbankmigrationen für Benutzer mit mehreren Mandanten orchestriert.
- **`static/` & `templates/`**: Reine HTML/CSS/JS-Frontend-Ansichten, Stylesheets und Dashboard-Bildschirme.
- **`saas_docs/`**: Betriebsrichtlinien und Verwaltungsanweisungen für die Plattform.

## Lokale Konfigurations- und Verpackungsdateien
Um die entkoppelte modulare Kompilierung zu unterstützen, enthält dieses Verzeichnis seine eigenen, eigenständigen Paketdateien:
- **`web.spec`**: PyInstaller-Spezifikationsdatei speziell für das Packen des SaaS-Webportals.
- **`build.py`**: Lokales Python-Build-Skript, das PyInstaller-Befehle ausführt, die auf „web.spec“ abzielen. (Der globale Orchestrator befindet sich in „scripts/build.py“).
- **`file_version_info.txt`**: Metadaten auf Betriebssystemebene, die die Version der ausführbaren Datei (v9.0.0.0), Urheberrechte und Beschreibungen definieren.
- **`installer_script.iss`**: Lokale Inno-Setup-Konfiguration zum Verpacken der kompilierten SaaS-Webanwendung.

## Wichtige Hinweise zur Architektur
- **Kein GUI-Overhead**: Streng isoliert von PySide6- und Qt-Komponenten, um effizient auf Headless-Produktionsservern zu laufen.
- **Micro-Gateway-Routing**: Delegiert intensive Generierung und Einbettung von Abfragen an die zugrunde liegende „Server/“-Schicht.

## Ausführbare Zusammenstellung
So kompilieren Sie die eigenständige Binärdatei „SaaS_Web_Portal.exe“ mit PyInstaller:
„Bash
pyinstaller web.spec
„