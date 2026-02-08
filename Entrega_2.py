import json
import logging
from datetime import datetime

# Configuracion del sistema de logs para registrar errores
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# --- CLASES ---

class Heroe:
    """
    Clase principal que representa a un miembro normal del gremio.
    """
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        self.tipo = "Normal" # Nos ayuda a diferenciar clases al guardar

    def to_dict(self):
        """Convierte el objeto en un diccionario para poder guardarlo en JSON."""
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "nivel": self.nivel
        }

    def __str__(self):
        return f"Recluta: {self.nombre} | Nivel: {self.nivel}"

# Clase Hija (Herencia)
class HeroeVeterano(Heroe):
    """
    Subclase para heroes especiales. Hereda de Heroe y añade batallas ganadas.
    """
    def __init__(self, nombre, nivel, batallas_ganadas):
        # Llamamos al constructor de la clase padre (Heroe)
        super().__init__(nombre, nivel)
        self.batallas_ganadas = batallas_ganadas
        self.tipo = "Veterano"

    def to_dict(self):
        # Primero obtenemos los datos base del padre
        data = super().to_dict()
        # Añadimos el dato exclusivo de esta clase
        data["batallas_ganadas"] = self.batallas_ganadas
        return data

    def __str__(self):
        # Sobrescribimos el metodo para que se muestre diferente
        return f"[VETERANO] {self.nombre} | Nivel: {self.nivel} | Batallas: {self.batallas_ganadas}"

# --- GESTION DE ARCHIVOS ---

class GestionGremio:
    """
    Clase encargada de leer y escribir en el archivo JSON.
    """
    def __init__(self):
        self.archivo = "datos_gremio.json"

    def cargar(self):
        """Lee el JSON y convierte los datos en una lista de objetos."""
        try:
            f = open(self.archivo, 'r')
            contenido = json.load(f)
            f.close()
            
            # Sacamos la lista de items del diccionario global
            datos_lista = contenido.get("items", [])
            
            lista_objetos = []
            for d in datos_lista:
                # Logica para saber que tipo de objeto crear (Polimorfismo)
                if d.get("tipo") == "Veterano":
                    h = HeroeVeterano(d['nombre'], d['nivel'], d['batallas_ganadas'])
                else:
                    h = Heroe(d['nombre'], d['nivel'])
                lista_objetos.append(h)
                
            print(f"Datos cargados. Fecha: {contenido.get('fecha_ultimo_guardado', '-')}")
            return lista_objetos
            
        except FileNotFoundError:
            # Si el archivo no existe, devolvemos una lista vacia
            return []
        except Exception as e:
            print(f"Error al cargar: {e}")
            return []

    def guardar(self, lista_heroes):
        """Guarda la lista de objetos y la fecha actual en el JSON."""
        try:
            # Paso 1: Convertir objetos a diccionarios
            lista_dicts = []
            for h in lista_heroes:
                lista_dicts.append(h.to_dict())
            
            # Paso 2: Crear estructura con metadatos (fecha)
            datos_globales = {
                "fecha_ultimo_guardado": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "items": lista_dicts
            }

            f = open(self.archivo, 'w')
            json.dump(datos_globales, f, indent=4)
            f.close()
        except Exception as e:
            print(f"Error al guardar: {e}")

# --- FUNCIONES DEL PROGRAMA ---

def añadir_heroe(lista, gestor):
    """Pide datos al usuario y añade un nuevo heroe a la lista."""
    print("\n--- NUEVO HEROE ---")
    print("1. Recluta Normal")
    print("2. Veterano")
    tipo = input("Opcion (1/2): ")
    
    nom = input("Nombre: ")
    if nom == "":
        print("El nombre es obligatorio.")
        return

    try:
        niv = int(input("Nivel: "))
        
        # Dependiendo de la opcion creamos una clase u otra
        if tipo == "2":
            batallas = int(input("Batallas ganadas: "))
            nuevo = HeroeVeterano(nom, niv, batallas)
        else:
            nuevo = Heroe(nom, niv)
            
        lista.append(nuevo)
        gestor.guardar(lista) # Guardamos cada vez que hay cambios
        print("Guardado correctamente.")
        
    except ValueError:
        print("Error: Introduce numeros validos.")

def buscar_heroe(lista):
    """Busca heroes por nombre (busqueda parcial) y muestra resultados."""
    print("\n--- BUSCAR ---")
    texto = input("Nombre a buscar: ").lower()
    encontrados = []

    for h in lista:
        # Busqueda parcial: miramos si el texto esta DENTRO del nombre
        if texto in h.nombre.lower():
            encontrados.append(h)

    if len(encontrados) > 0:
        print(f"\nResultados ({len(encontrados)}):")
        for h in encontrados:
            print(h)
    else:
        print("No se encontraron coincidencias.")
        # Registramos el fallo en el log
        logging.info(f"Busqueda sin exito: '{texto}'")

def generar_reporte(lista):
    """Muestra estadisticas y la lista ordenada."""
    print("\n--- INFORME ---")
    if len(lista) == 0:
        print("La lista esta vacia.")
        return

    # 1. Ordenar por nivel (de mayor a menor)
    # Usamos lambda para indicar que queremos ordenar usando el atributo 'nivel'
    lista_ordenada = sorted(lista, key=lambda x: x.nivel, reverse=True)
    
    print("Ranking por Nivel:")
    for h in lista_ordenada:
        print(f"- {h.nombre} (Nv. {h.nivel})")

    # 2. Calcular promedio
    suma_niveles = 0
    for h in lista:
        suma_niveles = suma_niveles + h.nivel
    
    promedio = suma_niveles / len(lista)
    
    # 3. Contar cuantos veteranos hay usando isinstance
    num_veteranos = 0
    for h in lista:
        if isinstance(h, HeroeVeterano):
            num_veteranos = num_veteranos + 1

    print("\nResumen:")
    print(f"Total heroes: {len(lista)}")
    print(f"Nivel medio: {promedio:.2f}")
    print(f"Veteranos: {num_veteranos}")

def eliminar_heroe(lista, gestor):
    """Busca un heroe por nombre exacto y lo elimina."""
    print("\n--- ELIMINAR ---")
    buscar = input("Nombre completo: ")
    for h in lista:
        if h.nombre.lower() == buscar.lower():
            lista.remove(h)
            gestor.guardar(lista)
            print("Eliminado.")
            return
    print("No existe.")

# --- MENU ---

def menu():
    gestor = GestionGremio()
    mi_plantilla = gestor.cargar()
    
    while True:
        print("\n=== GREMIO ===")
        print("1. Añadir")
        print("2. Buscar")
        print("3. Informe")
        print("4. Eliminar")
        print("5. Salir")
        
        opcion = input("Elige: ")
        
        if opcion == "1": añadir_heroe(mi_plantilla, gestor)
        elif opcion == "2": buscar_heroe(mi_plantilla)
        elif opcion == "3": generar_reporte(mi_plantilla)
        elif opcion == "4": eliminar_heroe(mi_plantilla, gestor)
        elif opcion == "5":
            gestor.guardar(mi_plantilla)
            print("Saliendo...")
            break
        else:
            print("Opcion incorrecta.")

if __name__ == "__main__":
    menu()
