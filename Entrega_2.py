import json
import logging
from datetime import datetime

# Configuracion del log (Requisito: Logging y Examen Ej.4)
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# --- 1. CLASES Y HERENCIA (Requisito: POO y Examen Ej.1) ---

class Heroe:
    """
    Clase base que representa un elemento principal del proyecto (Jugador/Personaje).
    """
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        self.tipo = "Normal" # Necesario para reconstruir el objeto al leer JSON

    def to_dict(self):
        """Convierte el objeto a diccionario para guardarlo en JSON."""
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "nivel": self.nivel
        }

    def __str__(self):
        return f"Recluta: {self.nombre} | Nivel: {self.nivel}"

class HeroeVeterano(Heroe):
    """
    Subclase (Herencia). Añade un atributo extra 'batallas_ganadas'.
    """
    def __init__(self, nombre, nivel, batallas_ganadas):
        super().__init__(nombre, nivel) # Aprovechamos el init del padre
        self.batallas_ganadas = batallas_ganadas
        self.tipo = "Veterano"

    def to_dict(self):
        # Usamos el diccionario del padre y añadimos lo nuestro
        data = super().to_dict()
        data["batallas_ganadas"] = self.batallas_ganadas
        return data

    def __str__(self):
        return f"[VETERANO] {self.nombre} | Nivel: {self.nivel} | Batallas: {self.batallas_ganadas}"

# --- 2. GESTIÓN DE FICHEROS (Requisito: JSON y Examen Ej.2) ---

class GestionGremio:
    """
    Clase encargada de la persistencia de datos (Guardar/Cargar).
    """
    def __init__(self):
        self.archivo = "datos_gremio.json"

    def cargar(self):
        """Lee el JSON y convierte los diccionarios en objetos Heroe o HeroeVeterano."""
        try:
            f = open(self.archivo, 'r')
            contenido = json.load(f)
            f.close()
            
            # Recuperamos la lista dentro de la estructura global
            datos_lista = contenido.get("items", [])
            
            lista_objetos = []
            for d in datos_lista:
                # Logica para instanciar la clase correcta
                if d.get("tipo") == "Veterano":
                    h = HeroeVeterano(d['nombre'], d['nivel'], d['batallas_ganadas'])
                else:
                    h = Heroe(d['nombre'], d['nivel'])
                lista_objetos.append(h)
                
            print(f"--> Datos cargados. Ultimo guardado: {contenido.get('fecha_ultimo_guardado', '-')}")
            return lista_objetos
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error al cargar: {e}")
            return []

    def guardar(self, lista_heroes):
        """Guarda la lista y la fecha actual en el JSON (Estructura global)."""
        try:
            lista_dicts = []
            for h in lista_heroes:
                lista_dicts.append(h.to_dict())
            
            # Estructura compleja pedida en el examen (fecha + items)
            datos_globales = {
                "fecha_ultimo_guardado": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "items": lista_dicts
            }

            f = open(self.archivo, 'w')
            json.dump(datos_globales, f, indent=4)
            f.close()
        except Exception as e:
            print(f"Error al guardar: {e}")

# --- 3. FUNCIONES PRINCIPALES (Requisito: 5 funciones obligatorias) ---

def insertar_heroe(lista, gestor):
    """
    Funcion 1: Añadir elemento.
    Pregunta tipo (Normal/Especial) y valida inputs.
    """
    print("\n--- NUEVO REGISTRO ---")
    print("1. Recluta Normal")
    print("2. Veterano (Clase Especial)")
    tipo = input("Elige opcion: ")
    
    nom = input("Nombre: ")
    if nom == "":
        print("Error: El nombre no puede estar vacio.")
        return

    try:
        niv = int(input("Nivel: ")) # Try/Except para validar entero
        
        if tipo == "2":
            batallas = int(input("Batallas ganadas: "))
            nuevo = HeroeVeterano(nom, niv, batallas)
        else:
            nuevo = Heroe(nom, niv)
            
        lista.append(nuevo)
        gestor.guardar(lista)
        print("Heroe añadido con exito.")
        
    except ValueError:
        print("Error: Debes introducir un numero valido para el nivel/batallas.")

def buscar_heroe(lista):
    """
    Funcion 2: Buscar elemento.
    Implementa Busqueda Parcial y Logging (Examen Ej.4).
    """
    print("\n--- BUSCADOR ---")
    texto = input("Introduce nombre (o parte del nombre): ").lower()
    encontrados = []

    for h in lista:
        if texto in h.nombre.lower():
            encontrados.append(h)

    if len(encontrados) > 0:
        print(f"\nSe han encontrado {len(encontrados)} coincidencias:")
        for h in encontrados:
            print(h)
    else:
        print("No se ha encontrado nadie.")
        logging.info(f"Busqueda fallida: '{texto}'")

def modificar_heroe(lista, gestor):
    """
    Funcion 3: Modificar elemento.
    Permite cambiar el nivel de un heroe existente.
    """
    print("\n--- MODIFICAR NIVEL ---")
    buscado = input("Nombre exacto del heroe a modificar: ")
    
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            print(f"Encontrado: {h}")
            try:
                nuevo_nivel = int(input("Introduce el nuevo nivel: "))
                h.nivel = nuevo_nivel
                gestor.guardar(lista)
                print("Nivel actualizado correctamente.")
                return
            except ValueError:
                print("Error: El nivel debe ser un numero.")
                return
                
    print("Error: No existe un heroe con ese nombre.")

def eliminar_heroe(lista, gestor):
    """
    Funcion 4: Eliminar elemento.
    Borra un heroe de la lista si existe.
    """
    print("\n--- ELIMINAR ---")
    buscado = input("Nombre del heroe a expulsar: ")
    
    for h in lista:
        if h.nombre.lower() == buscado.lower():
            lista.remove(h)
            gestor.guardar(lista)
            print(f"{h.nombre} ha sido eliminado del gremio.")
            return
            
    print("No se encontro ese nombre.")

def mostrar_todos_reporte(lista):
    """
    Funcion 5: Mostrar todos (Formato Reporte).
    Cumple 'Mostrar todos' del proyecto y 'Reporte' del Examen Ej.3.
    """
    print("\n--- INFORME DEL GREMIO ---")
    if not lista:
        print("El gremio esta vacio.")
        return

    # Ordenacion (Examen: sorted + lambda)
    lista_ordenada = sorted(lista, key=lambda x: x.nivel, reverse=True)
    
    print("LISTADO (Ordenado por Nivel):")
    for h in lista_ordenada:
        print(f"- {h.nombre} (Nivel {h.nivel})")

    # Calculos estadisticos (Examen)
    suma_niveles = 0
    num_veteranos = 0
    for h in lista:
        suma_niveles = suma_niveles + h.nivel
        if isinstance(h, HeroeVeterano):
            num_veteranos = num_veteranos + 1
            
    promedio = suma_niveles / len(lista)

    print("\nESTADISTICAS:")
    print(f"Total miembros: {len(lista)}")
    print(f"Nivel promedio: {promedio:.2f}")
    print(f"Veteranos en filas: {num_veteranos}")

# --- 4. MENU INTERACTIVO ---

def menu():
    gestor = GestionGremio()
    mi_plantilla = gestor.cargar()
    
    while True:
        print("\n=== GESTION DE GREMIO (PROYECTO FINAL) ===")
        print("1. Añadir Heroe")
        print("2. Buscar Heroe")
        print("3. Modificar Heroe")
        print("4. Eliminar Heroe")
        print("5. Mostrar Informe (Listado)")
        print("6. Salir")
        
        opcion = input("Selecciona una opcion: ")
        
        if opcion == "1": insertar_heroe(mi_plantilla, gestor)
        elif opcion == "2": buscar_heroe(mi_plantilla)
        elif opcion == "3": modificar_heroe(mi_plantilla, gestor)
        elif opcion == "4": eliminar_heroe(mi_plantilla, gestor)
        elif opcion == "5": mostrar_todos_reporte(mi_plantilla)
        elif opcion == "6":
            gestor.guardar(mi_plantilla)
            print("Guardando datos... ¡Adios!")
            break
        else:
            print("Opcion no valida. Intentalo de nuevo.")

if __name__ == "__main__":
    menu()
