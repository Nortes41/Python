import json
import logging

# --- CONFIGURACIÓN DEL LOGGING ---
# level=logging.INFO significa que guardará INFO, WARNING y ERROR.
# Si pusieramos level=logging.ERROR, solo guardaría los errores.
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Nombre del archivo donde se guardan los datos
NOMBRE_FICHERO = "datos_gremio.json"

# --- FUNCIONES DE ARCHIVOS ---

def cargar_datos_json():
    """Carga los datos del fichero. Si no existe, devuelve lista vacia."""
    try:
        fichero = open(NOMBRE_FICHERO, 'r')
        datos = json.load(fichero)
        fichero.close()
        # INFO: Para decir que la carga ha ido bien
        logging.info("Datos cargados correctamente.")
        return datos
    except:
        # INFO: No es un error grave, solo es la primera vez que se usa
        logging.info("Archivo no encontrado. Empezamos lista nueva.")
        return []

def guardar_datos_json(datos):
    """Guarda la lista en el fichero."""
    try:
        fichero = open(NOMBRE_FICHERO, 'w')
        json.dump(datos, fichero, indent=4)
        fichero.close()
    except:
        # ERROR: Si falla el guardado es un problema grave
        print("Error al guardar.")
        logging.error("Fallo crítico al intentar guardar en disco.")

# --- FUNCIONES DEL GREMIO ---

def insertar_elemento(lista_heroes):
    print("\n--- RECLUTAR ---")
    nombre = input("Nombre del héroe: ")
    
    if nombre == "":
        print("El nombre no puede estar vacío.")
        return

    try:
        nivel = int(input("Nivel inicial (número): "))
        
        nuevo = {"nombre": nombre, "nivel": nivel}
        lista_heroes.append(nuevo)
        
        guardar_datos_json(lista_heroes)
        print("Añadido con éxito.")
        
        # INFO: Una acción normal completada con éxito
        logging.info(f"Nuevo recluta añadido: {nombre}")
        
    except ValueError:
        print("Error: El nivel debe ser un número.")
        # ERROR: El usuario metió un dato inválido y saltó el try/except
        logging.error("Error al insertar: El usuario escribió texto en el nivel.")

def buscar_elemento(lista_heroes):
    print("\n--- BUSCAR ---")
    buscado = input("¿A quién buscas?: ")
    encontrado = False
    
    for heroe in lista_heroes:
        if heroe["nombre"].lower() == buscado.lower():
            print(f"Encontrado: {heroe['nombre']} (Lv {heroe['nivel']})")
            encontrado = True
            # INFO: Búsqueda exitosa
            logging.info(f"Búsqueda realizada con éxito: {buscado}")
            break
            
    if encontrado == False:
        print("No está en la lista.")
        # INFO: Búsqueda sin resultados (es información útil, no un error)
        logging.info(f"Búsqueda sin resultados: {buscado}")

def modificar_elemento(lista_heroes):
    print("\n--- ENTRENAR ---")
    buscado = input("¿A quién entrenas?: ")
    encontrado = False
    
    for heroe in lista_heroes:
        if heroe["nombre"].lower() == buscado.lower():
            encontrado = True
            try:
                nuevo_nivel = int(input("Nuevo nivel: "))
                heroe["nivel"] = nuevo_nivel
                guardar_datos_json(lista_heroes)
                print("Nivel actualizado.")
                
                # INFO: Modificación exitosa
                logging.info(f"Héroe modificado: {heroe['nombre']} ahora es Lv {nuevo_nivel}")
                
            except ValueError:
                print("Error de número.")
                # ERROR: Fallo al meter el dato
                logging.error(f"Error al modificar a {buscado}: Nivel incorrecto.")
            break
    
    if encontrado == False:
        print("No encontrado.")

def eliminar_elemento(lista_heroes):
    print("\n--- EXPULSAR ---")
    buscado = input("¿A quién expulsas?: ")
    encontrado = False
    
    for heroe in lista_heroes:
        if heroe["nombre"].lower() == buscado.lower():
            lista_heroes.remove(heroe)
            guardar_datos_json(lista_heroes)
            print("Expulsado.")
            encontrado = True
            
            # WARNING: ¡OJO! Esto es una acción destructiva (borrar datos)
            logging.warning(f"Héroe eliminado definitivamente: {buscado}")
            break
            
    if encontrado == False:
        print("No se puede borrar, no existe.")

def mostrar_todos(lista_heroes):
    print("\n--- LISTA ---")
    if len(lista_heroes) == 0:
        print("Gremio vacío.")
    else:
        for heroe in lista_heroes:
            print(f"- {heroe['nombre']} (Nivel {heroe['nivel']})")

# --- MENÚ ---

def menu():
    mis_heroes = cargar_datos_json()
    
    while True:
        print("\n1.Añadir 2.Buscar 3.Modificar 4.Eliminar 5.Ver 6.Salir")
        op = input("Opción: ")
        
        if op == "1": insertar_elemento(mis_heroes)
        elif op == "2": buscar_elemento(mis_heroes)
        elif op == "3": modificar_elemento(mis_heroes)
        elif op == "4": eliminar_elemento(mis_heroes)
        elif op == "5": mostrar_todos(mis_heroes)
        elif op == "6": 
            print("Adios.")
            logging.info("--- Sesión cerrada ---")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    menu()
