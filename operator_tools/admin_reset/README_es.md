# Restablecimiento de credenciales de administrador universal (v9.0)

Esta herramienta permite a los administradores de servidores restablecer de forma segura las credenciales de administrador maestro en todos los entornos.

## Características
- **Ejecución en modo dual**:
  - **Modo GUI**: genera un cuadro de diálogo del asistente PySide6 de alta fidelidad para entornos de escritorio locales.
  - **CLI/Modo sin cabeza**: omite por completo las dependencias de la GUI utilizando `--headless` o `--cli`, lo que lo hace perfecto para terminales SSH remotas, scripts de automatización y trabajos cron.
- **Opciones de contraseña dinámica**:
  - `--random-password`: Genera una contraseña alfanumérica segura y aleatoria de 12 caracteres.
  - `--custom-password "your_password"`: establece una cadena de contraseña personalizada y específica.
  - El valor predeterminado es la contraseña "admin" si no se especifica ninguna opción.
- **Detección automática del controlador**: lee automáticamente la información de conexión y resuelve los parámetros del controlador desde `saas/config.ini` o el entorno.

## Archivos de configuración y empaquetado locales
Para admitir la compilación modular desacoplada, este directorio contiene sus propios archivos de empaquetado independientes:
- **`reset_admin.spec`**: archivo de especificaciones de PyInstaller específico para empaquetar la herramienta de reinicio del administrador.
- **`build.py`**: script de compilación local de Python que ejecuta comandos de PyInstaller dirigidos a `reset_admin.spec`. (El orquestador global está en `scripts/build.py`).
- **`file_version_info.txt`**: metadatos a nivel del sistema operativo que definen la versión del ejecutable (v9.0.0.0), derechos de autor y descripciones.
- **`installer_script.iss`**: configuración local de Inno Setup para empaquetar la herramienta de reinicio de administrador compilada.

## Ejecución

### CLI/modo sin cabeza:
```golpecito
python reset_admin.py --sin cabeza
```

### Especificaciones de PyInstaller
Para compilar el binario independiente `Admin_Reset` usando PyInstaller:
```golpecito
pyinstaller reset_admin.spec
```
Esto aísla la funcionalidad de restablecimiento de contraseña de las distribuciones de clientes públicos, manteniendo seguras las claves administrativas.