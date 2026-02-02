import json
import logging

# Configuro el log para que guarde lo que pasa en el programa
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Clase para el objeto Héroe (el molde)
class Heroe:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

# Clase para manejar el archivo JSON y no tener las funciones sueltas
class GestionGremio:
    def __init__(self):
        self.archivo = "datos_gremio.json"

    def cargar(self):
        try:
            f = open(self.archivo, 'r')
            datos = json.load(f)
            f.close()
            
            # Paso los diccionarios del JSON a mi lista de objetos
            lista = []
            for d in datos:
                lista.append(Heroe(d['nombre'], d['nivel']))
            return lista
        except:
            # Si no hay archivo, devuelvo la lista vacía para empezar
            return []

    def guardar(self, lista_heroes):
        try:
            f = open(self.archivo, 'w')
            # El JSON solo entiende diccionarios, así que convierto los objetos
            datos_finales = []
            for h in lista_heroes:
                datos_finales.append({"nombre": h.nombre, "nivel": h.nivel})
            
            json.dump(datos_finales, f, indent=4)
            f.close()
        except:
            print("Error al guardar en el archivo.")

# --- FUNCIONES DEL PROGRAMA ---

def añadir_heroe(lista, gestor):
    print("\n--- NUEVO RECLUTA ---")
    nom = input("Nombre: ")
    if nom != "":
        try:
            niv = int(input("Nivel: "))
            nuevo = Heroe(nom, niv)
            lista.append(nuevo)
            gestor.guardar(lista)
            print("Guardado con éxito.")
        except:
            print("Error: El nivel tiene que ser un número.")

def buscar_heroe(lista):
    print("\n--- BUSCADOR ---")
    buscado = input("¿A quién buscas?: ")
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            print(f"Encontrado: {h.nombre} (Nivel {h.nivel})")
            return # Salgo de la función si lo encuentro
    print("No se ha encontrado.")

def entrenar_heroe(lista, gestor):
    print("\n--- ENTRENAMIENTO ---")
    buscado = input("¿A quién quieres subir de nivel?: ")
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            try:
                nuevo_niv = int(input("Nuevo nivel: "))
                h.nivel = nuevo_niv
                gestor.guardar(lista)
                print("Nivel actualizado.")
                return
            except:
                print("Número no válido.")
                return
    print("Héroe no encontrado.")

def expulsar_heroe(lista, gestor):
    print("\n--- EXPULSAR ---")
    buscado = input("¿A quién echamos?: ")
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            lista.remove(h)
            gestor.guardar(lista)
            print("Eliminado del gremio.")
            return
    print("No existe ese nombre.")

def ver_gremio(lista):
    print("\n--- MIEMBROS ACTUALES ---")
    if len(lista) == 0:
        print("No hay nadie en el gremio.")
    else:
        for h in lista:
            print(f"- {h.nombre} | Nivel: {h.nivel}")

# --- INICIO DEL PROGRAMA ---

def menu():
    gestor = GestionGremio()
    mis_heroes = gestor.cargar()
    
    while True:
        print("\n1.Añadir | 2.Buscar | 3.Entrenar | 4.Expulsar | 5.Lista | 6.Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1": añadir_heroe(mis_heroes, gestor)
        elif opcion == "2": buscar_heroe(mis_heroes)
        elif opcion == "3": entrenar_heroe(mis_heroes, gestor)
        elif opcion == "4": expulsar_heroe(mis_heroes, gestor)
        elif opcion == "5": ver_gremio(mis_heroes)
        elif opcion == "6":
            print("Cerrando el programa...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
