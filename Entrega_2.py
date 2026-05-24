import json
import logging
from datetime import datetime

logging.basicConfig(
    filename='registro_gremio.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

HABILIDADES_DISPONIBLES = {
    "Normal": ["Espadazo", "Escudo", "Flechazo", "Curación básica", "Sigilo", "Golpe en área"],
    "Veterano": ["Golpe maestro", "Torbellino", "Barrera arcana", "Llamada de guerra",
                 "Contraataque", "Ráfaga de fuego", "Manto de sombras", "Juicio divino"]
}


class Heroe:
    def __init__(self, nombre, nivel, habilidades=None):
        self.nombre = nombre
        self.nivel = nivel
        self.tipo = "Normal"
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


class GestionGremio:
    def __init__(self):
        self.archivo = "datos_gremio.json"

    def cargar(self):
        try:
            f = open(self.archivo, 'r')
            contenido = json.load(f)
            f.close()

            datos_lista = contenido.get("items", [])
            lista_objetos = []

            for d in datos_lista:
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


def elegir_habilidades(tipo_heroe):
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

    heroe_max = max(lista, key=lambda x: x.nivel)
    heroe_min = min(lista, key=lambda x: x.nivel)
    print(f"\nHéroe de mayor nivel: {heroe_max.nombre} (Nv. {heroe_max.nivel})")
    print(f"Héroe de menor nivel: {heroe_min.nombre} (Nv. {heroe_min.nivel})")

    max_habs = max(len(h.habilidades) for h in lista)
    if max_habs > 0:
        heroes_max_habs = [h for h in lista if len(h.habilidades) == max_habs]
        print(f"\nHéroe(s) con más habilidades ({max_habs}):")
        for h in heroes_max_habs:
            print(f"  - {h.nombre}: {', '.join(h.habilidades)}")

    veteranos = [h for h in lista if isinstance(h, HeroeVeterano)]
    if veteranos:
        print("\nVeteranos (por batallas):")
        for v in sorted(veteranos, key=lambda x: x.batallas_ganadas, reverse=True):
            print(f"  - {v.nombre} | Nivel: {v.nivel} | Batallas: {v.batallas_ganadas}")


def filtrar_por_nivel(lista):
    print("\n--- FILTRAR POR NIVEL ---")
    try:
        nivel_min = int(input("Nivel mínimo: "))
        resultado = [h for h in lista if h.nivel >= nivel_min]
        if resultado:
            print(f"\nHéroes con nivel {nivel_min} o superior:")
            for h in resultado:
                print(h)
        else:
            print("No hay héroes con ese nivel mínimo.")
    except ValueError:
        print("Error: escribe un número.")


def buscar_por_habilidad(lista):
    print("\n--- BUSCAR POR HABILIDAD ---")
    hab = input("Habilidad a buscar: ").lower()
    resultado = [h for h in lista if any(hab in habilidad.lower() for habilidad in h.habilidades)]

    if resultado:
        print(f"\nEncontrados {len(resultado)}:")
        for h in resultado:
            print(h)
    else:
        print("No hay héroes con esa habilidad.")


def contar_habilidades(lista):
    print("\n--- HABILIDADES ---")
    con_habilidad = [h for h in lista if h.habilidades]
    sin_habilidad = [h for h in lista if not h.habilidades]
    print(f"Héroes con habilidades: {len(con_habilidad)}")
    print(f"Héroes sin habilidades: {len(sin_habilidad)}")


def subir_nivel_todos(lista, gestor):
    print("\n--- SUBIR NIVEL A TODOS ---")
    try:
        cantidad = int(input("¿Cuántos niveles subir? "))
        for h in lista:
            h.nivel += cantidad
        gestor.guardar(lista)
        print(f"Actualizados {len(lista)} héroes.")
        logging.info(f"Subida de nivel masiva: +{cantidad} a todos los héroes.")
    except ValueError:
        print("Error: escribe un número.")


def exportar_informe(lista):
    print("\n--- EXPORTAR INFORME ---")
    if not lista:
        print("La lista está vacía, no hay nada que exportar.")
        return
    try:
        f = open("informe_gremio.txt", "w", encoding="utf-8")
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"INFORME DEL GREMIO - {fecha}\n")
        f.write("=" * 40 + "\n")
        for h in sorted(lista, key=lambda x: x.nivel, reverse=True):
            hab_str = ", ".join(h.habilidades) if h.habilidades else "Ninguna"
            f.write(f"{h.nombre} | Nivel: {h.nivel} | Habilidades: {hab_str}\n")
        f.close()
        print("Informe exportado a 'informe_gremio.txt'.")
        logging.info("Informe exportado a .txt")
    except Exception as e:
        print(f"Error al exportar: {e}")


def menu_busqueda(lista):
    print("\n--- BÚSQUEDA CON FILTROS ---")
    print("1. Por nombre")
    print("2. Por nivel mínimo")
    print("3. Por tipo (Normal/Veterano)")
    print("4. Por habilidad")
    opcion = input("Elige filtro: ")

    if opcion == "1":
        texto = input("Nombre a buscar: ").lower()
        resultado = [h for h in lista if texto in h.nombre.lower()]

    elif opcion == "2":
        try:
            nivel_min = int(input("Nivel mínimo: "))
            resultado = [h for h in lista if h.nivel >= nivel_min]
        except ValueError:
            print("Error: escribe un número.")
            return

    elif opcion == "3":
        tipo = input("Tipo (Normal/Veterano): ").capitalize()
        resultado = [h for h in lista if h.tipo == tipo]

    elif opcion == "4":
        hab = input("Habilidad a buscar: ").lower()
        resultado = [h for h in lista if any(hab in habilidad.lower() for habilidad in h.habilidades)]

    else:
        print("Opción incorrecta.")
        return

    if resultado:
        print(f"\nEncontrados {len(resultado)}:")
        for h in resultado:
            print(h)
    else:
        print("No se encontró ningún héroe con ese filtro.")


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
        print("7. Filtrar por nivel")
        print("8. Buscar por habilidad")
        print("9. Contar habilidades")
        print("10. Subir nivel a todos")
        print("11. Exportar informe a .txt")
        print("12. Búsqueda con filtros")
        print("13. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":    insertar_heroe(mi_plantilla, gestor)
        elif opcion == "2":  buscar_heroe(mi_plantilla)
        elif opcion == "3":  modificar_heroe(mi_plantilla, gestor)
        elif opcion == "4":  eliminar_heroe(mi_plantilla, gestor)
        elif opcion == "5":  mostrar_informe(mi_plantilla)
        elif opcion == "6":  gestionar_habilidades(mi_plantilla, gestor)
        elif opcion == "7":  filtrar_por_nivel(mi_plantilla)
        elif opcion == "8":  buscar_por_habilidad(mi_plantilla)
        elif opcion == "9":  contar_habilidades(mi_plantilla)
        elif opcion == "10": subir_nivel_todos(mi_plantilla, gestor)
        elif opcion == "11": exportar_informe(mi_plantilla)
        elif opcion == "12": menu_busqueda(mi_plantilla)
        elif opcion == "13":
            gestor.guardar(mi_plantilla)
            print("Guardando... ¡Adiós!")
            logging.info("--- Fin del programa ---")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    menu()
