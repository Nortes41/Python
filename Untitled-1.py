"""
Sistema de Gremio de Heroes.
Gestiona una lista de diccionarios (nombre y nivel).
"""

heroes = []

def reclutar():
    """Pide nombre y nivel. Valida entrada."""
    nom = input("Nombre: ")
    # Validacion basica
    if not nom:
        print("Nombre obligatorio.")
        return

    try:
        # Validacion int
        lv = int(input("Nivel: "))
        heroes.append({"nom": nom, "lv": lv})
        print("Añadido.")
    except ValueError:
        print("Error: El nivel debe ser numero.")

def buscar():
    """Busca heroe por nombre."""
    b = input("A quien buscas?: ")
    for h in heroes:
        if h["nom"] == b:
            print(f"Heroe: {h['nom']}, Nivel: {h['lv']}")
            return
    print("No encontrado.")

def entrenar():
    """Modifica el nivel de un heroe."""
    b = input("A quien entrenas?: ")
    for h in heroes:
        if h["nom"] == b:
            try:
                nuevo = int(input("Nuevo nivel: "))
                h["lv"] = nuevo
                print("Nivel actualizado.")
            except ValueError:
                print("Error de numero.")
            return
    print("No encontrado.")

def expulsar():
    """Elimina heroe de la lista."""
    b = input("A quien echas?: ")
    for h in heroes:
        if h["nom"] == b:
            heroes.remove(h)
            print("Expulsado.")
            return
    print("No encontrado.")

def ver_todos():
    """Muestra la lista completa."""
    print("LISTA DEL GREMIO:")
    if not heroes:
        print("Vacio.")
    for h in heroes:
        print(f"- {h['nom']} (Lv {h['lv']})")

def menu():
    while True:
        # Menu simple en una linea
        print("\n1.Reclutar 2.Buscar 3.Entrenar 4.Expulsar 5.Ver 6.Salir")
        op = input("Opcion: ")

        if op == "1": reclutar()
        elif op == "2": buscar()
        elif op == "3": entrenar()
        elif op == "4": expulsar()
        elif op == "5": ver_todos()
        elif op == "6": break
        else: print("Opcion mal.")

if __name__ == "__main__":
    menu()
