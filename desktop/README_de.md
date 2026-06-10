# Lokale Admin-GUI und Desktop-Client (v9.0)

In diesem Verzeichnis befindet sich die eigenständige grafische Benutzeroberfläche von PySide6, die als „Mission Control“-Panel des lokalen Administrators fungiert.

## Verzeichnisstruktur
- **`main.py`**: Einstiegspunkt, der native Anwendungsstartparameter, CLI-Handler und das Laden von Fenstergrenzen orchestriert.
- **`ui/`**: PySide6-Fensteransichtscontroller, Thread-Schleifen, benutzerdefinierte Widget-Bindungen und Ereignishandler.
- **`ui_designer/`**: Reine XML-`.ui`-Beschreibungsschemata, die von Qt Designer generiert wurden.
- **`headless/`**: Lokale CLI-Chat-Eingabeaufforderungen und Hintergrund-Terminalschleifen.

## Lokale Konfigurations- und Verpackungsdateien
Um die entkoppelte modulare Kompilierung zu unterstützen, enthält dieses Verzeichnis seine eigenen, eigenständigen Paketdateien:
- **`desktop.spec`**: PyInstaller-Spezifikationsdatei speziell für das Packen des Desktop-Clients.
- **`build.py`**: Lokales Python-Build-Skript, das PyInstaller-Befehle ausführt, die auf „desktop.spec“ abzielen. (Der globale Orchestrator befindet sich in „scripts/build.py“).
- **`file_version_info.txt`**: Metadaten auf Betriebssystemebene, die die Version der ausführbaren Datei (v9.0.0.0), Urheberrechte und Beschreibungen definieren.
- **`installer_script.iss`**: Lokale Inno-Setup-Konfiguration zum Packen der kompilierten Desktop-Anwendung.

## Hauptmerkmale
- **Umgehungskontrolle**: Konfiguriert aktive Speicherkonfigurationen, Datenbanken und LLM-Anbieter direkt lokal, ohne auf das öffentliche API-Gateway angewiesen zu sein.
- **SSH-Tunnel-Manager**: Stellt sofort verschlüsselte SSH/VPN-Weiterleitungsverbindungen zu Remote-Cloud-Clustern her (Redis, Postgres, Godmode API).
- **Kein SaaS-Packaging-Bloat**: Saubere Kompilierung mit PyInstaller unter strikter Ignorierung von „Web/“-Routing-Assets.

## Ausführbare Zusammenstellung
So kompilieren Sie die eigenständige Binärdatei „Synora_Studio.exe“ mit PyInstaller:
„Bash
pyinstaller desktop.spec
„