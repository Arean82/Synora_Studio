# Headless Chat und Terminal-CLI-Engine

Dieses Verzeichnis implementiert die Chat-Schleife der interaktiven Befehlszeilenschnittstelle (CLI) und die Verwaltung von Anmeldeinformationen, sodass Entwickler direkt vom Terminal aus mit LLM-Anbietern interagieren können.

## Dateistruktur
- **`auth.py`**: Verarbeitet API-Schlüsseleingaben und Authentifizierungssitzungen für CLI-Clients.
- **`engine.py`**: Der Ausführungskontext, der die Nur-Text-Schleife ausführt.
- **`models.py`**: Logik zum Anzeigen und Austauschen aktiver Modelle in der CLI.
- **`worker.py`**: Orchestriert Streaming-Generierungsblöcke und Druckformatierung.

## Nutzung
Führen Sie im Stammverzeichnis Folgendes aus, um die CLI-Konsole aufzurufen:
„Bash
python desktop/main.py --cli
„
Hinweis: Dieses Modul ist aus Remote-Server-Bereitstellungsumgebungen strikt ausgeschlossen, um die Produktions-Hosting-Pakete auf ein Minimum zu beschränken.