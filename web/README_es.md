# Portal web SaaS y puerta de enlace multiinquilino (v9.0)

Este directorio alberga el portal de aplicaciones web, el panel de control de enrutamiento de bases de datos, los motores dinámicos de espacio aislado de inquilinos y las interfaces de administración de clientes SaaS.

## Estructura del directorio
- **`app.py`**: el controlador de aplicaciones principal de Flask que maneja rutas, autenticaciones JWT, inicios de sesión de inquilinos, flujos de sesión y puntos finales REST.
- **`run_web.py`**: Ejecutor de script estándar que importa la instancia de `app` y activa el bucle del servidor.
- **`core/`**: módulos auxiliares principales de SaaS (por ejemplo, `launcher.py`, `agent_manager.py`, `config_manager.py`, `tenant_db.py`).
- **`tenant_drivers/`**: middleware que organiza aislamientos de esquemas y migraciones de bases de datos en la nube para usuarios multiinquilino.
- **`static/` & `templates/`**: vistas frontales, hojas de estilo y pantallas de panel HTML/CSS/JS puro.
- **`saas_docs/`**: Pautas operativas de la plataforma e instrucciones administrativas.

## Archivos de configuración y empaquetado locales
Para admitir la compilación modular desacoplada, este directorio contiene sus propios archivos de empaquetado independientes:
- **`web.spec`**: archivo de especificaciones de PyInstaller específico para empaquetar el portal web SaaS.
- **`build.py`**: script de compilación local de Python que ejecuta comandos de PyInstaller dirigidos a `web.spec`. (El orquestador global está en `scripts/build.py`).
- **`file_version_info.txt`**: metadatos a nivel del sistema operativo que definen la versión del ejecutable (v9.0.0.0), derechos de autor y descripciones.
- **`installer_script.iss`**: Configuración local de Inno Setup para empaquetar la aplicación web SaaS compilada.

## Notas clave de arquitectura
- **Cero gastos generales de GUI**: Estrictamente aislado de los componentes PySide6 y Qt para ejecutarse de manera eficiente en servidores de producción sin cabeza.
- **Enrutamiento de micropuerta de enlace**: delega la generación intensiva y la incorporación de consultas a la capa subyacente `servidor/`.

## Compilación ejecutable
Para compilar el binario independiente `SaaS_Web_Portal.exe` usando PyInstaller:
```golpecito
pyinstaller web.spec
```