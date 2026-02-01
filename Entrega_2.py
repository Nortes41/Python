import json
import logging

# --- CONFIGURACIÓN DEL LOGGING ---
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Creamos una clase para que cada héroe sea un "objeto" con sus propios datos
class Heroe:
    def __init__(self, nombre, nivel):
        self.nombre = nombre  # Guardamos el nombre en el objeto
        self.nivel = nivel    # Guardamos el nivel en el objeto

# Clase para agrupar las funciones que manejan el archivo JSON
class GestionGremio:
    def __init__(self):
        self.NOMBRE_FICHERO = "datos_gremio.json"

    def cargar_datos_json(self):
        """Lee el JSON y convierte los diccionarios en una lista de objetos Heroe."""
        try:
            fichero = open(self.NOMBRE_FICHERO, 'r')
            datos_viejos = json.load(fichero)
            fichero.close()
            
            # Pasamos los datos del JSON a nuestra lista de objetos
            lista_objetos = []
            for d in datos_viejos:
                lista_objetos.append(Heroe(d['nombre'], d['nivel']))
            
            logging.info("Datos cargados correctamente.")
            return lista_objetos
        except:
            logging.info("Archivo no encontrado. Empezamos lista nueva.")
            return []

    def guardar_datos_json(self, lista_heroes):
        """Convierte los objetos Heroe a diccionarios para poder guardarlos en el JSON."""
        try:
            fichero = open(self.NOMBRE_FICHERO, 'w')
            datos_convertidos = []
            for h in lista_heroes:
                # El JSON no entiende de objetos, así que se lo pasamos como diccionario
                datos_convertidos.append({"nombre": h.nombre, "nivel": h.nivel})
            
            json.dump(datos_convertidos, fichero, indent=4)
            fichero.close()
        except:
            print("Error al guardar.")
            logging.error("Fallo crítico al intentar guardar en disco.")

# --- FUNCIONES DEL GREMIO ---

def insertar_elemento(lista_heroes, herramientas):
    print("\n--- RECLUTAR ---")
    nombre = input("Nombre del héroe: ")
    if nombre == "": return

    try:
        nivel = int(input("Nivel inicial: "))
        # Creamos un nuevo objeto Heroe y lo añadimos a la lista
        nuevo = Heroe(nombre, nivel)
        lista_heroes.append(nuevo)
        
        herramientas.guardar_datos_json(lista_heroes)
        print("Añadido con éxito.")
        logging.info(f"Nuevo recluta: {nombre}")
    except ValueError:
        print("Error: El nivel debe ser un número.")

def buscar_elemento(lista_heroes):
    print("\n--- BUSCAR ---")
    buscado = input("¿A quién buscas?: ")
    encontrado = False
    
    for h in lista_heroes:
        # Ahora usamos h.nombre (atributo del objeto) en vez de h["nombre"]
        if h.nombre.lower() == buscado.lower():
            print(f"Encontrado: {h.nombre} (Lv {h.nivel})")
            encontrado = True
            break
            
    if not encontrado:
        print("No está en la lista.")

def modificar_elemento(lista_heroes, herramientas):
    print("\n--- ENTRENAR ---")
    buscado = input("¿A quién modificas?: ")
    
    for h in lista_heroes:
        if h.nombre.lower() == buscado.lower():
            try:
                nuevo_nivel = int(input("Nuevo nivel: "))
                h.nivel = nuevo_nivel # Cambiamos el nivel directamente en el objeto
                herramientas.guardar_datos_json(lista_heroes)
                print("Nivel actualizado.")
                return
            except ValueError:
                print("Error de número.")
                return
    print("No encontrado.")

def eliminar_elemento(lista_heroes, herramientas):
    print("\n--- EXPULSAR ---")
    buscado = input("¿A quién expulsas?: ")
    
    for h in lista_heroes:
        if h.nombre.lower() == buscado.lower():
            lista_heroes.remove(h) # Quitamos el objeto de la lista
            herramientas.guardar_datos_json(lista_heroes)
            print("Expulsado.")
            logging.warning(f"Eliminado: {buscado}")
            return
    print("No existe.")

def mostrar_todos(lista_heroes):
    print("\n--- LISTA ---")
    if not lista_heroes:
        print("Gremio vacío.")
    else:
        for h in lista_heroes:
            # Imprimimos los datos usando los puntos (.) para acceder a las variables del objeto
            print(f"- {h.nombre} (Nivel {h.nivel})")

# --- MENÚ ---

def menu():
    # 'herramientas' es el objeto que tiene las funciones de guardar/cargar
    herramientas = GestionGremio()
    mis_heroes = herramientas.cargar_datos_json()
    
    while True:
        print("\n1.Añadir 2.Buscar 3.Modificar 4.Eliminar 5.Ver 6.Salir")
        op = input("Opción: ")
        
        if op == "1": insertar_elemento(mis_heroes, herramientas)
        elif op == "2": buscar_elemento(mis_heroes)
        elif op == "3": modificar_elemento(mis_heroes, herramientas)
        elif op == "4": eliminar_elemento(mis_heroes, herramientas)
        elif op == "5": mostrar_todos(mis_heroes)
        elif op == "6": 
            print("Adios.")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    menu()
