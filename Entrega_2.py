import json
import logging

# Configuración básica del logging (para registrar eventos)
# Esto crea un archivo .log para ver qué ha pasado en el programa
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

# Nombre del archivo donde guardaremos los datos
NOMBRE_FICHERO = "datos_gremio.json"

# --- FUNCIONES DE ARCHIVOS (JSON) ---

def cargar_datos_json():
    """Intenta cargar la lista del archivo JSON. Si falla, devuelve lista vacía."""
    try:
        # Intentamos abrir el archivo en modo lectura ('r')
        fichero = open(NOMBRE_FICHERO, 'r')
        datos = json.load(fichero)
        fichero.close()
        logging.info("Se han cargado los datos correctamente.")
        return datos
    except:
        # Si da error (porque no existe el archivo aun), devolvemos lista vacia
        logging.info("No se encontró archivo o dio error. Empezamos de cero.")
        return []

def guardar_datos_json(datos):
    """Guarda la lista actual en el archivo JSON."""
    try:
        # Abrimos en modo escritura ('w')
        fichero = open(NOMBRE_FICHERO, 'w')
        # indent=4 es para que se vea ordenado en el archivo
        json.dump(datos, fichero, indent=4)
        fichero.close()
    except:
        print("Error: No se pudo guardar el archivo.")
        logging.error("Error critico al intentar guardar.")

# --- FUNCIONES DEL EJERCICIO ---

def insertar_elemento(lista_heroes):
    """Pide datos, valida y añade un nuevo heroe."""
    print("\n--- NUEVO RECLUTA ---")
    nombre = input("Dime el nombre del héroe: ")
    
    # Validacion simple: que no esté vacío
    if nombre == "":
        print("Error: El nombre no puede estar vacío.")
        return

    try:
        # Validamos que el nivel sea un numero (Try/Except obligatorio 1)
        nivel = int(input("Dime su nivel (número): "))
        
        # Creamos el diccionario del heroe
        nuevo_heroe = {
            "nombre": nombre,
            "nivel": nivel
        }
        
        # Lo añadimos a la lista y guardamos
        lista_heroes.append(nuevo_heroe)
        guardar_datos_json(lista_heroes)
        
        print("Heroe reclutado con éxito.")
        logging.info(f"Se ha insertado el heroe: {nombre}")
        
    except ValueError:
        print("Error: Tienes que poner un número en el nivel.")
        logging.error("Error al insertar: El usuario no puso un número.")

def buscar_elemento(lista_heroes):
    """Busca un heroe por su nombre."""
    print("\n--- BUSCADOR ---")
    nombre_buscado = input("¿A quién buscas?: ")
    
    # Usamos una variable para saber si lo encontramos
    encontrado = False
    
    for heroe in lista_heroes:
        # Comparamos los nombres (ponemos todo en minusculas para que no falle)
        if heroe["nombre"].lower() == nombre_buscado.lower():
            print(f"Encontrado: {heroe['nombre']} - Nivel: {heroe['nivel']}")
            encontrado = True
            logging.info(f"Busqueda exitosa de: {nombre_buscado}")
            # Si lo encontramos, dejamos de buscar
            break
            
    if encontrado == False:
        print("No he encontrado a nadie con ese nombre.")

def modificar_elemento(lista_heroes):
    """Cambia el nivel de un heroe existente."""
    print("\n--- ENTRENAMIENTO (MODIFICAR) ---")
    nombre_buscado = input("¿A quién quieres entrenar?: ")
    
    encontrado = False
    
    for heroe in lista_heroes:
        if heroe["nombre"].lower() == nombre_buscado.lower():
            encontrado = True
            print(f"Nivel actual de {heroe['nombre']}: {heroe['nivel']}")
            
            try:
                # Control de errores al pedir el nuevo nivel (Try/Except 2)
                nuevo_nivel = int(input("Nuevo nivel: "))
                heroe["nivel"] = nuevo_nivel
                
                guardar_datos_json(lista_heroes)
                print("Nivel actualizado.")
                logging.info(f"Se ha modificado a {heroe['nombre']} al nivel {nuevo_nivel}")
                
            except ValueError:
                print("Error: El nivel tiene que ser un número.")
                logging.error("Error al modificar: Dato no valido.")
            
            # Salimos del bucle
            break
            
    if encontrado == False:
        print("Ese héroe no está en el gremio.")

def eliminar_elemento(lista_heroes):
    """Borra un heroe de la lista."""
    print("\n--- EXPULSAR ---")
    nombre_borrar = input("¿A quién quieres expulsar?: ")
    
    encontrado = False
    
    for heroe in lista_heroes:
        if heroe["nombre"].lower() == nombre_borrar.lower():
            lista_heroes.remove(heroe)
            encontrado = True
            
            guardar_datos_json(lista_heroes)
            print(f"{nombre_borrar} ha sido expulsado.")
            logging.warning(f"Se ha eliminado al heroe: {nombre_borrar}")
            break
            
    if encontrado == False:
        print("No se puede borrar, no existe.")

def mostrar_todos(lista_heroes):
    """Muestra la lista completa de heroes."""
    print("\n--- LISTA DEL GREMIO ---")
    
    # Comprobamos si la lista está vacía
    if len(lista_heroes) == 0:
        print("No hay héroes todavía.")
    else:
        # Uso un contador manual, es más sencillo de entender
        contador = 1
        for heroe in lista_heroes:
            print(f"{contador}. {heroe['nombre']} (Nivel {heroe['nivel']})")
            contador = contador + 1

# --- MENU PRINCIPAL ---

def menu():
    # Cargamos los datos al principio
    mis_heroes = cargar_datos_json()
    
    while True:
        print("\n=== MENU GREMIO ===")
        print("1. Añadir elemento")
        print("2. Buscar elemento")
        print("3. Modificar elemento")
        print("4. Eliminar elemento")
        print("5. Mostrar todos")
        print("6. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            insertar_elemento(mis_heroes)
        elif opcion == "2":
            buscar_elemento(mis_heroes)
        elif opcion == "3":
            modificar_elemento(mis_heroes)
        elif opcion == "4":
            eliminar_elemento(mis_heroes)
        elif opcion == "5":
            mostrar_todos(mis_heroes)
        elif opcion == "6":
            print("Adios!")
            logging.info("Cierre del programa.")
            break
        else:
            print("Opción incorrecta, prueba otra vez.")

# Bloque principal para ejecutar
if __name__ == "__main__":
    menu()
