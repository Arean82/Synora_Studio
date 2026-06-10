# GUI de administración local y cliente de escritorio (v9.0)

Este directorio alberga la interfaz gráfica de usuario independiente de PySide6, que funciona como el panel de "Control de misión" del administrador local.

## Estructura del directorio
- **`main.py`**: punto de entrada que organiza los parámetros de inicio de la aplicación nativa, los controladores CLI y la carga de límites de ventana.
- **`ui/`**: controladores de vista de ventana de PySide6, bucles de subprocesos, enlaces de widgets personalizados y controladores de eventos.
- **`ui_designer/`**: esquemas de descripción XML puro `.ui` generados desde Qt Designer.
- **`headless/`**: mensajes de chat CLI local y bucles de terminal en segundo plano.

## Archivos de configuración y empaquetado locales
Para admitir la compilación modular desacoplada, este directorio contiene sus propios archivos de empaquetado independientes:
- **`desktop.spec`**: archivo de especificaciones de PyInstaller específico para empaquetar el cliente de escritorio.
- **`build.py`**: script de compilación local de Python que ejecuta comandos de PyInstaller dirigidos a `desktop.spec`. (El orquestador global está en `scripts/build.py`).
- **`file_version_info.txt`**: metadatos a nivel del sistema operativo que definen la versión del ejecutable (v9.0.0.0), derechos de autor y descripciones.
- **`installer_script.iss`**: Configuración local de Inno Setup para empaquetar la aplicación de escritorio compilada.

## Características clave
- **Omitir control**: configura directamente configuraciones de almacenamiento activo, bases de datos y proveedores de LLM localmente sin depender de la puerta de enlace API pública.
- **SSH Tunnel Manager**: establece instantáneamente conexiones de reenvío SSH/VPN cifradas a clústeres de nube remotos (Redis, Postgres, API Godmode).
- **Zero SaaS Packaging Bloat**: compila limpiamente usando PyInstaller ignorando estrictamente los activos de enrutamiento `web/`.

## Compilación ejecutable
Para compilar el binario independiente `Synora_Studio.exe` usando PyInstaller:
```golpecito
pyinstaller escritorio.spec
```