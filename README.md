# PROYECTO FINAL PYTHON: GESTIÓN DE GREMIO

**Nombre:** David Nortes Peñalver
**Curso:** 2025/2026
**Asignatura:** Programación

## Descripción del Proyecto
Este proyecto tiene como objetivo gestionar la información de un gremio de héroes (alta, baja, modificación y consulta). Se han aplicado todos los conocimientos del curso: POO, manejo de ficheros, estructuras de datos y control de errores.

Además, he decidido incluir los 4 ejercicios del examen práctico dentro del proyecto. No hacian falta pero los he hecho para practicar y entender mejor cómo funciona las cosas que me pedian.

## Funcionalidades

### 1. Gestión de Datos (CRUD)
El programa cuenta con un menú interactivo con las siguientes opciones:
* **Insertar:** Permite crear héroes Normales o Veteranos (uso de **Herencia**).
* **Buscar:** Localiza héroes por nombre. Incluye **búsqueda parcial** (ej. "ara" encuentra "Aragorn") y registro de errores en `log` (**Logging**).
* **Modificar:** Permite actualizar el nivel de un héroe existente.
* **Eliminar:** Borra un héroe de la base de datos.
* **Mostrar Informe:** Genera un listado completo.

### 2. Persistencia de Datos (JSON)
Los datos se guardan automáticamente en `datos_gremio.json`. 
* He cambiado la estructura para que guarde la lista de objetos y también la **fecha de la última modificación**.
* El sistema recupera automáticamente los datos al iniciar, diferenciando entre clases `Heroe` y `HeroeVeterano`.

### 3. Estadísticas y Ordenación
En la opción de "Mostrar Informe":
* Los héroes aparecen **ordenados por Nivel** (de mayor a menor).
* Se muestra el nivel promedio del gremio.
* Se contabiliza cuántos héroes son de la clase especial "Veterano".

## Estructura del Código
* `main.py`: Contiene toda la lógica, clases y funciones.
* `datos_gremio.json`: Archivo de almacenamiento.
* `registro_gremio.log`: Archivo de registro de búsquedas fallidas.

## Requisitos
* Python 3.x
* Librerías: `json`, `logging`, `datetime`.

## Ejecución
python main.py
