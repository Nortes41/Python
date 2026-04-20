import json
import logging
from datetime import datetime

logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Catalogo de habilidades disponibles por tipo de heroe
HABILIDADES_DISPONIBLES = {
    "Normal": ["Espadazo", "Escudo", "Flechazo", "Curación básica", "Sigilo", "Golpe en área"],
    "Veterano": ["Golpe maestro", "Torbellino", "Barrera arcana", "Llamada de guerra",
                 "Contraataque", "Ráfaga de fuego", "Manto de sombras", "Juicio divino"]
}

# --- CLASES Y OBJETOS ---

class Heroe:
    """Clase para los reclutas normales del gremio"""
    def __init__(self, nombre, nivel, habilidades=None):
        self.nombre = nombre
        self.nivel = nivel
        self.tipo = "Normal"
        # Si no se pasan habilidades, lista vacía
        self.habilidades = habilidades if habilidades is not None else []

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "nivel": self.nivel,
            "habilidades": self.habilidades
        }

    def __str__(self):
        hab_str = ", ".join(self.habilidades) if self.habilidades else "Ninguna"
        return f"Recluta: {self.nombre} | Nivel: {self.nivel} | Habilidades: [{hab_str}]"


class HeroeVeterano(Heroe):
    """Clase hija. Hereda de Heroe y tiene un dato extra (batallas)"""
    def __init__(self, nombre, nivel, batallas_ganadas, habilidades=None):
        super().__init__(nombre, nivel, habilidades)
        self.batallas_ganadas = batallas_ganadas
        self.tipo = "Veterano"

    def to_dict(self):
        data = super().to_dict()
        data["batallas_ganadas"] = self.batallas_ganadas
        return data

    def __str__(self):
        hab_str = ", ".join(self.habilidades) if self.habilidades else "Ninguna"
        return (f"[VETERANO] {self.nombre} | Nivel: {self.nivel} "
                f"| Batallas: {self.batallas_ganadas} | Habilidades: [{hab_str}]")


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

            datos_lista = contenido.get("items", [])
            lista_objetos = []

            for d in datos_lista:
                # Cargamos habilidades si existen (compatibilidad con archivos antiguos)
                habilidades = d.get("habilidades", [])

                if d.get("tipo") == "Veterano":
                    h = HeroeVeterano(d['nombre'], d['nivel'], d['batallas_ganadas'], habilidades)
                else:
                    h = Heroe(d['nombre'], d['nivel'], habilidades)
                lista_objetos.append(h)

            print(f"--> Datos cargados. Fecha guardado: {contenido.get('fecha_ultimo_guardado', '-')}")
            return lista_objetos

        except FileNotFoundError:
            logging.info("No hay archivo previo. Iniciando lista vacia.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            logging.error(f"Error grave cargando datos: {e}")
            return []

    def guardar(self, lista_heroes):
        """Guarda todo en el JSON con la fecha actual"""
        try:
            lista_dicts = [h.to_dict() for h in lista_heroes]

            datos_globales = {
                "fecha_ultimo_guardado": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "items": lista_dicts
            }

            f = open(self.archivo, 'w')
            json.dump(datos_globales, f, indent=4, ensure_ascii=False)
            f.close()
        except Exception as e:
            print(f"Error al guardar: {e}")
            logging.error(f"Error grave guardando datos: {e}")


# --- GESTION DE HABILIDADES ---

def elegir_habilidades(tipo_heroe):
    """Muestra el catálogo y permite elegir habilidades"""
    catalogo = HABILIDADES_DISPONIBLES.get(tipo_heroe, [])

    print(f"\nHabilidades disponibles para {tipo_heroe}:")
    for i, hab in enumerate(catalogo, 1):
        print(f"  {i}. {hab}")
    print("  0. Terminar selección")

    seleccionadas = []
    while True:
        try:
            opcion = int(input("Elige una habilidad (0 para terminar): "))
            if opcion == 0:
                break
            elif 1 <= opcion <= len(catalogo):
                hab = catalogo[opcion - 1]
                if hab in seleccionadas:
                    print("Esa habilidad ya está seleccionada.")
                else:
                    seleccionadas.append(hab)
                    print(f"  -> '{hab}' añadida.")
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Escribe un número.")

    return seleccionadas


def gestionar_habilidades(lista, gestor):
    """Menú para añadir o quitar habilidades a un héroe existente"""
    print("\n--- GESTIONAR HABILIDADES ---")
    buscado = input("Nombre exacto del héroe: ")

    for h in lista:
        if h.nombre.lower() == buscado.lower():
            print(f"\nHéroe: {h}")
            print("\nOpciones:")
            print("  1. Añadir habilidad")
            print("  2. Quitar habilidad")
            opcion = input("Elige: ")

            if opcion == "1":
                # Mostrar solo las que aún no tiene
                catalogo = HABILIDADES_DISPONIBLES.get(h.tipo, [])
                disponibles = [hab for hab in catalogo if hab not in h.habilidades]

                if not disponibles:
                    print("Ya tiene todas las habilidades disponibles para su tipo.")
                    return

                print(f"\nHabilidades que puede aprender:")
                for i, hab in enumerate(disponibles, 1):
                    print(f"  {i}. {hab}")

                try:
                    num = int(input("Elige una (número): "))
                    if 1 <= num <= len(disponibles):
                        nueva = disponibles[num - 1]
                        h.habilidades.append(nueva)
                        gestor.guardar(lista)
                        print(f"'{nueva}' añadida a {h.nombre}.")
                        logging.info(f"Habilidad añadida: {h.nombre} aprendió '{nueva}'")
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Escribe un número.")

            elif opcion == "2":
                if not h.habilidades:
                    print("Este héroe no tiene habilidades que quitar.")
                    return

                print(f"\nHabilidades actuales:")
                for i, hab in enumerate(h.habilidades, 1):
                    print(f"  {i}. {hab}")

                try:
                    num = int(input("Elige cuál quitar (número): "))
                    if 1 <= num <= len(h.habilidades):
                        eliminada = h.habilidades.pop(num - 1)
                        gestor.guardar(lista)
                        print(f"'{eliminada}' eliminada de {h.nombre}.")
                        logging.info(f"Habilidad eliminada: {h.nombre} perdió '{eliminada}'")
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Escribe un número.")
            else:
                print("Opción incorrecta.")
            return

    print("No existe ese héroe.")


# --- FUNCIONES DEL PROGRAMA ---

def insertar_heroe(lista, gestor):
    print("\n--- NUEVO HEROE ---")
    print("1. Recluta Normal")
    print("2. Veterano")
    opcion = input("Elige: ")

    nom = input("Nombre: ")
    if nom == "":
        print("El nombre no puede estar vacío.")
        return

    try:
        niv = int(input("Nivel: "))

        # Preguntar si quiere asignar habilidades ahora
        tipo = "Veterano" if opcion == "2" else "Normal"
        print(f"\n¿Quieres asignar habilidades ahora?")
        print("  1. Sí")
        print("  2. No (se pueden añadir después)")
        resp = input("Elige: ")
        habilidades = elegir_habilidades(tipo) if resp == "1" else []

        if opcion == "2":
            batallas = int(input("Batallas ganadas: "))
            nuevo = HeroeVeterano(nom, niv, batallas, habilidades)
        else:
            nuevo = Heroe(nom, niv, habilidades)

        lista.append(nuevo)
        gestor.guardar(lista)
        print("Guardado.")
        logging.info(f"Alta: {nuevo.nombre} (Tipo: {nuevo.tipo}, Habilidades: {nuevo.habilidades})")

    except ValueError:
        print("Error: Tienes que poner números.")


def buscar_heroe(lista):
    print("\n--- BUSCAR ---")
    texto = input("Nombre a buscar: ").lower()
    encontrados = [h for h in lista if texto in h.nombre.lower()]

    if encontrados:
        print(f"\nEncontrado {len(encontrados)}:")
        for h in encontrados:
            print(h)
    else:
        print("No he encontrado nada.")
        logging.info(f"Búsqueda sin éxito: '{texto}'")


def modificar_heroe(lista, gestor):
    print("\n--- MODIFICAR NIVEL ---")
    buscado = input("Nombre exacto del héroe: ")

    for h in lista:
        if h.nombre.lower() == buscado.lower():
            print(f"Encontrado: {h}")
            try:
                nuevo_nivel = int(input("Nuevo nivel: "))
                nivel_viejo = h.nivel
                h.nivel = nuevo_nivel
                gestor.guardar(lista)
                print("Nivel cambiado.")
                logging.info(f"Modificación: {h.nombre} pasó de nivel {nivel_viejo} a {nuevo_nivel}")
                return
            except ValueError:
                print("Error: El nivel tiene que ser un número.")
                return
    print("No existe ese héroe.")


def eliminar_heroe(lista, gestor):
    print("\n--- ELIMINAR ---")
    buscado = input("Nombre del héroe: ")

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
    if not lista:
        print("La lista está vacía.")
        return

    lista_ordenada = sorted(lista, key=lambda x: x.nivel, reverse=True)

    print("Ranking por Nivel:")
    for h in lista_ordenada:
        print(f"- {h.nombre} (Nv. {h.nivel})")

    suma_niveles = sum(h.nivel for h in lista)
    num_veteranos = sum(1 for h in lista if isinstance(h, HeroeVeterano))
    media = suma_niveles / len(lista)

    # Habilidad más común
    todas_habs = []
    for h in lista:
        todas_habs.extend(h.habilidades)

    print("\nEstadísticas:")
    print(f"Total héroes: {len(lista)}")
    print(f"Nivel medio: {media:.2f}")
    print(f"Veteranos: {num_veteranos}")

    if todas_habs:
        hab_mas_comun = max(set(todas_habs), key=todas_habs.count)
        print(f"Habilidad más usada: {hab_mas_comun} ({todas_habs.count(hab_mas_comun)} héroes)")

        heroes_sin_hab = sum(1 for h in lista if not h.habilidades)
        if heroes_sin_hab:
            print(f"Héroes sin habilidades: {heroes_sin_hab}")
    else:
        print("Ningún héroe tiene habilidades aún.")


# --- MENU PRINCIPAL ---

def menu():
    logging.info("--- Inicio del programa ---")

    gestor = GestionGremio()
    mi_plantilla = gestor.cargar()

    while True:
        print("\n=== GREMIO DE HEROES ===")
        print("1. Añadir")
        print("2. Buscar")
        print("3. Modificar nivel")
        print("4. Eliminar")
        print("5. Informe")
        print("6. Gestionar habilidades")
        print("7. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":   insertar_heroe(mi_plantilla, gestor)
        elif opcion == "2": buscar_heroe(mi_plantilla)
        elif opcion == "3": modificar_heroe(mi_plantilla, gestor)
        elif opcion == "4": eliminar_heroe(mi_plantilla, gestor)
        elif opcion == "5": mostrar_informe(mi_plantilla)
        elif opcion == "6": gestionar_habilidades(mi_plantilla, gestor)
        elif opcion == "7":
            gestor.guardar(mi_plantilla)
            print("Guardando... ¡Adiós!")
            logging.info("--- Fin del programa ---")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    menu()
