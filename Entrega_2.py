import json
import logging

# --- CONFIGURACIÓN DEL LOGGING ---
logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

class Heroe:
    """Clase que representa a un miembro del gremio."""
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    def to_dict(self):
        """Convierte el objeto a diccionario para guardarlo en JSON."""
        return {"nombre": self.nombre, "nivel": self.nivel}

    @staticmethod
    def from_dict(datos):
        """Crea un objeto Heroe a partir de un diccionario."""
        return Heroe(datos["nombre"], datos["nivel"])

    def __str__(self):
        return f"- {self.nombre} (Nivel {self.nivel})"


class Gremio:
    """Clase que gestiona la lista de héroes y persistencia de datos."""
    def __init__(self, archivo="datos_gremio.json"):
        self.archivo = archivo
        self.lista_heroes = self._cargar_datos()

    def _cargar_datos(self):
        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                logging.info("Datos cargados correctamente.")
                # Convertimos cada diccionario del JSON en un objeto Heroe
                return [Heroe.from_dict(h) for h in datos]
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("Archivo no encontrado o vacío. Lista nueva iniciada.")
            return []

    def guardar(self):
        try:
            with open(self.archivo, 'w') as f:
                # Convertimos los objetos Heroe de vuelta a diccionarios
                datos_dict = [h.to_dict() for h in self.lista_heroes]
                json.dump(datos_dict, f, indent=4)
        except Exception as e:
            print("Error al guardar.")
            logging.error(f"Fallo crítico al guardar: {e}")

    def reclutar(self, nombre, nivel):
        nuevo = Heroe(nombre, nivel)
        self.lista_heroes.append(nuevo)
        self.guardar()
        logging.info(f"Nuevo recluta: {nombre}")

    def buscar(self, nombre):
        for h in self.lista_heroes:
            if h.nombre.lower() == nombre.lower():
                return h
        return None

    def expulsar(self, nombre):
        heroe = self.buscar(nombre)
        if heroe:
            self.lista_heroes.remove(heroe)
            self.guardar()
            logging.warning(f"Héroe eliminado: {nombre}")
            return True
        return False

# --- INTERFAZ DE USUARIO (MENÚ) ---

def menu():
    mi_gremio = Gremio()
    
    while True:
        print("\n1.Añadir 2.Buscar 3.Modificar 4.Eliminar 5.Ver 6.Salir")
        op = input("Opción: ")

        if op == "1":
            nom = input("Nombre: ")
            try:
                niv = int(input("Nivel: "))
                mi_gremio.reclutar(nom, niv)
                print("Añadido.")
            except ValueError:
                logging.error("Nivel inválido en inserción.")
                print("Error: El nivel debe ser un número.")

        elif op == "2":
            buscado = input("¿A quién buscas?: ")
            h = mi_gremio.buscar(buscado)
            if h:
                print(f"Encontrado: {h}")
                logging.info(f"Búsqueda exitosa: {buscado}")
            else:
                print("No encontrado.")
                logging.info(f"Búsqueda fallida: {buscado}")

        elif op == "3":
            buscado = input("¿A quién entrenas?: ")
            h = mi_gremio.buscar(buscado)
            if h:
                try:
                    nuevo_niv = int(input("Nuevo nivel: "))
                    h.nivel = nuevo_niv
                    mi_gremio.guardar()
                    print("Actualizado.")
                    logging.info(f"Modificado: {h.nombre} a Lv {nuevo_niv}")
                except ValueError:
                    print("Nivel incorrecto.")
            else:
                print("No encontrado.")

        elif op == "4":
            buscado = input("¿A quién expulsas?: ")
            if mi_gremio.expulsar(buscado):
                print("Expulsado.")
            else:
                print("No existe.")

        elif op == "5":
            print("\n--- MIEMBROS DEL GREMIO ---")
            if not mi_gremio.lista_heroes:
                print("El gremio está vacío.")
            for h in mi_gremio.lista_heroes:
                print(h)

        elif op == "6":
            logging.info("--- Sesión cerrada ---")
            break

if __name__ == "__main__":
    menu()
