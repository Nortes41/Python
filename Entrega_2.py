import json
import logging
from datetime import datetime

# Configuramos el archivo donde se guardan los errores y eventos
# Esto crea el archivo 'registro_gremio.log' al lado del programa
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# --- CLASES Y OBJETOS ---

class Heroe:
    """Clase para los reclutas normales del gremio"""
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        self.tipo = "Normal" # Esto me sirve luego para saber cual es cual

    def to_dict(self):
        # Convierto el objeto a diccionario para poder guardarlo en el JSON
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "nivel": self.nivel
        }

    def __str__(self):
        return f"Recluta: {self.nombre} | Nivel: {self.nivel}"

class HeroeVeterano(Heroe):
    """Clase hija. Hereda de Heroe y tiene un dato extra (batallas)"""
    def __init__(self, nombre, nivel, batallas_ganadas):
        # Llamo al constructor de la clase padre (Heroe)
        super().__init__(nombre, nivel)
        self.batallas_ganadas = batallas_ganadas
        self.tipo = "Veterano"

    def to_dict(self):
        # Pillo el diccionario del padre y le añado lo mio
        data = super().to_dict()
        data["batallas_ganadas"] = self.batallas_ganadas
        return data

    def __str__(self):
        return f"[VETERANO] {self.nombre} | Nivel: {self.nivel} | Batallas: {self.batallas_ganadas}"

# --- GESTION DEL ARCHIVO JSON ---

class GestionGremio:
    def __init__(self):
        self.archivo = "datos_gremio.json"

    def cargar(self):
        """Intenta leer el archivo JSON y devuelve una lista de objetos"""
        try:
            f = open(self.archivo, 'r')
            contenido = json.load(f)
            f.close()
            
            # Saco la lista de la clave "items"
            datos_lista = contenido.get("items", [])
            
            lista_objetos = []
            for d in datos_lista:
                # Aqui miro si es Veterano o Normal para crear el objeto correcto
                if d.get("tipo") == "Veterano":
                    h = HeroeVeterano(d['nombre'], d['nivel'], d['batallas_ganadas'])
                else:
                    h = Heroe(d['nombre'], d['nivel'])
                lista_objetos.append(h)
            
            print(f"--> Datos cargados. Fecha guardado: {contenido.get('fecha_ultimo_guardado', '-')}")
            return lista_objetos
            
        except FileNotFoundError:
            # Si no existe el archivo, no pasa nada, empezamos de cero
            logging.info("No hay archivo previo. Iniciando lista vacia.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            logging.error(f"Error grave cargando datos: {e}")
            return []

    def guardar(self, lista_heroes):
        """Guarda todo en el JSON con la fecha actual"""
        try:
            # Paso 1: Convertir la lista de objetos a diccionarios
            lista_dicts = []
            for h in lista_heroes:
                lista_dicts.append(h.to_dict())
            
            # Paso 2: Preparar la estructura con la fecha
            datos_globales = {
                "fecha_ultimo_guardado": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "items": lista_dicts
            }

            # Paso 3: Escribir en el archivo
            f = open(self.archivo, 'w')
            json.dump(datos_globales, f, indent=4)
            f.close()
        except Exception as e:
            print(f"Error al guardar: {e}")
            logging.error(f"Error grave guardando datos: {e}")

# --- FUNCIONES DEL PROGRAMA ---

def insertar_heroe(lista, gestor):
    print("\n--- NUEVO HEROE ---")
    print("1. Recluta Normal")
    print("2. Veterano")
    opcion = input("Elige: ")
    
    nom = input("Nombre: ")
    if nom == "":
        print("El nombre no puede estar vacio.")
        return

    try:
        niv = int(input("Nivel: "))
        
        if opcion == "2":
            batallas = int(input("Batallas ganadas: "))
            nuevo = HeroeVeterano(nom, niv, batallas)
        else:
            nuevo = Heroe(nom, niv)
            
        lista.append(nuevo)
        gestor.guardar(lista)
        print("Guardado.")
        
        # Guardo en el log que ha entrado alguien
        logging.info(f"Alta: {nuevo.nombre} (Tipo: {nuevo.tipo})")
        
    except ValueError:
        print("Error: Tienes que poner numeros.")

def buscar_heroe(lista):
    print("\n--- BUSCAR ---")
    # Lo paso a minusculas para que la busqueda sea mas facil
    texto = input("Nombre a buscar: ").lower()
    encontrados = []

    for h in lista:
        # Busqueda parcial (si el texto esta dentro del nombre)
        if texto in h.nombre.lower():
            encontrados.append(h)

    if len(encontrados) > 0:
        print(f"\nHe encontrado {len(encontrados)}:")
        for h in encontrados:
            print(h)
    else:
        print("No he encontrado nada.")
        logging.info(f"Busqueda sin exito: '{texto}'")

def modificar_heroe(lista, gestor):
    print("\n--- MODIFICAR NIVEL ---")
    buscado = input("Nombre exacto del heroe: ")
    
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            print(f"Encontrado: {h}")
            try:
                nuevo_nivel = int(input("Nuevo nivel: "))
                nivel_viejo = h.nivel
                h.nivel = nuevo_nivel # Actualizo el dato
                gestor.guardar(lista)
                print("Nivel cambiado.")
                
                logging.info(f"Modificacion: {h.nombre} paso de nivel {nivel_viejo} a {nuevo_nivel}")
                return
            except ValueError:
                print("Error: El nivel tiene que ser un numero.")
                return
    print("No existe ese heroe.")

def eliminar_heroe(lista, gestor):
    print("\n--- ELIMINAR ---")
    buscado = input("Nombre del heroe: ")
    
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            lista.remove(h)
            gestor.guardar(lista)
            print("Eliminado.")
            
            logging.info(f"Baja: {h.nombre} eliminado.")
            return
    print("No lo encuentro.")

def mostrar_informe(lista):
    print("\n--- INFORME ---")
    if len(lista) == 0:
        print("La lista esta vacia.")
        return

    # Ordeno la lista por nivel (de mas a menos)
    lista_ordenada = sorted(lista, key=lambda x: x.nivel, reverse=True)
    
    print("Ranking por Nivel:")
    for h in lista_ordenada:
        print(f"- {h.nombre} (Nv. {h.nivel})")

    # Calculo la media y cuento veteranos
    suma_niveles = 0
    num_veteranos = 0
    for h in lista:
        suma_niveles = suma_niveles + h.nivel
        if isinstance(h, HeroeVeterano):
            num_veteranos = num_veteranos + 1
            
    media = suma_niveles / len(lista)

    print("\nEstadisticas:")
    print(f"Total heroes: {len(lista)}")
    print(f"Nivel medio: {media:.2f}")
    print(f"Veteranos: {num_veteranos}")

# --- MENU PRINCIPAL ---

def menu():
    logging.info("--- Inicio del programa ---")
    
    gestor = GestionGremio()
    mi_plantilla = gestor.cargar()
    
    while True:
        print("\n=== GREMIO DE HEROES ===")
        print("1. Añadir")
        print("2. Buscar")
        print("3. Modificar")
        print("4. Eliminar")
        print("5. Informe")
        print("6. Salir")
        
        opcion = input("Elige una opcion: ")
        
        if opcion == "1": insertar_heroe(mi_plantilla, gestor)
        elif opcion == "2": buscar_heroe(mi_plantilla)
        elif opcion == "3": modificar_heroe(mi_plantilla, gestor)
        elif opcion == "4": eliminar_heroe(mi_plantilla, gestor)
        elif opcion == "5": mostrar_informe(mi_plantilla)
        elif opcion == "6":
            gestor.guardar(mi_plantilla)
            print("Guardando... Adios!")
            logging.info("--- Fin del programa ---")
            break
        else:
            print("Opcion incorrecta.")

if __name__ == "__main__":
    menu()
