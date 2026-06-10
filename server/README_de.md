# Zentrale Headless Core Engine (Backend-Server) (v9.0)

Dieses Verzeichnis enthält die Kern-Backend-Logik, die KI-Laufzeitorchestrierung, Vektordatenbankschnittstellen und Hintergrundaufgaben. Es ist streng **UI-agnostisch** und enthält keine Desktop-UI- oder Webroutendefinitionen.

## Verzeichnisstruktur
- **`Logik/`**: Einheitlicher LLM-Client-Router (Google/NVIDIA/OpenAI/Custom), Einbettungsdienste, Datenbankverbindungsadapter (PostgreSQL/Turso) und Hintergrund-Chat-Worker-Warteschlangen.
- **`utils/`**: Hilfsprogramme für gemeinsame Einstellungen, sichere Auflöser für Anmeldeinformationen, Speicherpfadkonfigurationen und systemweite Konstanten.
- **`workers/`**: Asynchrone Aufgabenkonsumenten, die Vektoreinbettungen, Token-Nutzungsverfolgung, Hintergrundprotokollaufnahme und Indizierung ausführen.
- **`resources/`**: Statische Metadatenassets wie das Anbieterschema und die Modellregistrierungsmanifeste.
- **`run_server.py`**: Führt die eigenständige Server-Routing-API (Port 5000) für lokale Offline-Gateways aus.

## Lokale Konfigurations- und Verpackungsdateien
Um die entkoppelte modulare Kompilierung zu unterstützen, enthält dieses Verzeichnis seine eigenen, eigenständigen Paketdateien:
- **`server.spec`**: PyInstaller-Spezifikationsdatei speziell für das Packen des API-Servers.
- **`build.py`**: Lokales Python-Build-Skript, das PyInstaller-Befehle ausführt, die auf „server.spec“ abzielen. (Der globale Orchestrator befindet sich in „scripts/build.py“).
- **`file_version_info.txt`**: Metadaten auf Betriebssystemebene, die die Version der ausführbaren Datei (v9.0.0.0), Urheberrechte und Beschreibungen definieren.
- **`installer_script.iss`**: Lokale Inno-Setup-Konfiguration zum Packen der kompilierten Serveranwendung.

## Funktionen
- **Intelligenter LLM-Router**: Polymorphe Schnittstelle, die Anfragen dynamisch löst.
- **Entkoppeltes RAG**: Vektoren direkt mit entkoppelten Einbettungsdienstprogrammen zwischenspeichern.
- **Secure Storage Gateway**: Integriert Turso-Datenbank-Bootstrap mit dynamischen Failovers.

## Ausführbare Zusammenstellung
So kompilieren Sie die eigenständige Binärdatei „API_Server.exe“ mit PyInstaller:
„Bash
pyinstaller server.spec
„