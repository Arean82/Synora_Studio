# Instalador complementario de demonio de servicio y operación (v9.0)

Companion Operation es una utilidad administrativa de modo dual que facilita la migración de plataformas, reubicaciones de datos locales, copias de seguridad de bases de datos, configuración de red/web y generación de demonios de servicios del sistema.

## Características
- **Reubicación de bases de datos**: Migra de forma autónoma todos los esquemas y datos desde entornos de arranque locales (Turso/libSQL SQLite) hasta clústeres empresariales de producción (PostgreSQL).
- **Configuración de red/web**: actualice mediante programación el enlace del host y los puertos para el portal web SaaS a través de GUI o CLI.
- **Generación de servicios automatizada (instalador Daemon)**:
  - Genera configuraciones de demonios en segundo plano nativos.
  - **Windows (NSSM)**: genera un script de PowerShell (`install_<nombre>.ps1`) que descarga automáticamente NSSM, configura la ejecución, bloquea permisos e instala la API como un servicio de Windows.
  - **Linux (systemd)**: genera un archivo `.service` y un script bash automatizado (`install_<nombre>.sh`) que configura systemd, establece usuarios de servicios dedicados y configura el refuerzo de seguridad (como `PrivateTmp`, `ProtectHome` y capacidades restringidas).
- **Ejecución en modo dual**:
  - **Modo GUI**: panel del asistente paso a paso de PySide6.
  - **Modo CLI**: asistente de terminal interactivo o acciones programables (por ejemplo, `--action=backup`).

## Archivos de configuración y empaquetado locales
Para admitir la compilación modular desacoplada, este directorio contiene sus propios archivos de empaquetado independientes:
- **`companion_operation.spec`**: archivo de especificaciones de PyInstaller específico para empaquetar la herramienta Companion Operation.
- **`build.py`**: script de compilación local de Python que ejecuta comandos de PyInstaller dirigidos a `companion_operation.spec`. (El orquestador global está en `scripts/build.py`).
- **`file_version_info.txt`**: metadatos a nivel del sistema operativo que definen la versión del ejecutable (v9.0.0.0), derechos de autor y descripciones.
- **`installer_script.iss`**: configuración local de Inno Setup para empaquetar la herramienta Companion Operation compilada.

## Ejecución

### Modo CLI:
```golpecito
python compañero_operación.py --sin cabeza
```

### Especificaciones de PyInstaller
Para compilar el binario independiente `Companion_Operation` usando PyInstaller:
```golpecito
pyinstallercompañero_operación.spec
```
Esto garantiza que las herramientas del operador privado se compilen por separado del paquete principal del usuario de escritorio.