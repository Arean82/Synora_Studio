# Motor CLI de terminal y chat sin cabeza

Este directorio implementa el bucle de chat interactivo de la interfaz de línea de comandos (CLI) y la administración de credenciales, lo que permite a los desarrolladores interactuar con los proveedores de LLM directamente desde la terminal.

## Estructura de archivos
- **`auth.py`**: Maneja entradas de claves API y sesiones de autenticación para clientes CLI.
- **`engine.py`**: el contexto de ejecución que ejecuta el bucle de solo texto.
- **`models.py`**: Lógica para mostrar e intercambiar modelos activos en la CLI.
- **`worker.py`**: organiza fragmentos de generación de streaming y formato de impresión.

## Uso
Ejecute lo siguiente desde el directorio raíz para ingresar a la consola CLI:
```golpecito
escritorio de Python/main.py --cli
```
Nota: Este módulo está estrictamente excluido de los entornos de implementación de servidores remotos para mantener los paquetes de alojamiento de producción al mínimo.