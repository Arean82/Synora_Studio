# Motor central sin cabeza (servidor backend) (v9.0)

Este directorio alberga la lógica central del backend, la orquestación del tiempo de ejecución de la IA, las interfaces de bases de datos vectoriales y las tareas en segundo plano. Es estrictamente **independiente de la interfaz de usuario** y no contiene definiciones de rutas web ni de interfaz de usuario de escritorio.

## Estructura del directorio
- **`logic/`**: enrutador de cliente LLM unificado (Google/NVIDIA/OpenAI/Custom), servicios de integración, adaptadores de conexión de bases de datos (PostgreSQL/Turso) y colas de trabajadores de chat en segundo plano.
- **`utils/`**: asistentes de configuración compartida, solucionadores de credenciales seguros, configuraciones de rutas de almacenamiento y constantes de todo el sistema.
- **`workers/`**: consumidores de tareas asincrónicas que ejecutan incrustaciones de vectores, seguimiento del uso de tokens, ingesta de registros en segundo plano e indexación.
- **`resources/`**: activos de metadatos estáticos, como el esquema de proveedores y los manifiestos de registro del modelo.
- **`run_server.py`**: ejecuta la API de enrutamiento del servidor independiente (puerto 5000) para puertas de enlace locales fuera de línea.

## Archivos de configuración y empaquetado locales
Para admitir la compilación modular desacoplada, este directorio contiene sus propios archivos de empaquetado independientes:
- **`server.spec`**: archivo de especificaciones de PyInstaller específico para empaquetar el servidor API.
- **`build.py`**: script de compilación local de Python que ejecuta comandos de PyInstaller dirigidos a `server.spec`. (El orquestador global está en `scripts/build.py`).
- **`file_version_info.txt`**: metadatos a nivel del sistema operativo que definen la versión del ejecutable (v9.0.0.0), derechos de autor y descripciones.
- **`installer_script.iss`**: Configuración local de Inno Setup para empaquetar la aplicación del servidor compilada.

## Características
- **Intelligent LLM Router**: Interfaz polimórfica que resuelve solicitudes de forma dinámica.
- **RAG desacoplado**: almacenamiento en caché de vectores directamente mediante utilidades de incrustación desacopladas.
- **Secure Storage Gateway**: integra el arranque de la base de datos de Turso con conmutación por error dinámica.

## Compilación ejecutable
Para compilar el binario independiente `API_Server.exe` usando PyInstaller:
```golpecito
servidor pyinstaller.spec
```