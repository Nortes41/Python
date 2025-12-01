"""
Gestor de stock simple.
Maneja una lista de diccionarios con referencia y valor.
"""

# Estructura principal
almacen = []

def alta_articulo():
    """Pide datos, valida y agrega al final de la lista."""
    print("\n>> NUEVO REGISTRO")
    ref = input("Referencia del articulo: ")
    
    # Validacion requerida: campo no vacio
    if len(ref) == 0:
        print("Error: Referencia vacia.")
        return

    try:
        val = float(input("Valor numerico: "))
        # Crea el diccionario
        item = {"ref": ref, "val": val}
        almacen.append(item)
        print(" Guardado.")
    except ValueError:
        # Control de errores 1
        print(" Error: No es un numero valido.")

def localizar_articulo():
    """Busca por referencia exacta e imprime."""
    print("\n>> BUSQUEDA")
    b = input("Cual buscas?: ")
    for x in almacen:
        if x["ref"] == b:
            print(f" Encontrado: {x['ref']} vale {x['val']}")
            return
    print("❌ No existe.")

def editar_articulo():
    """Busca y permite cambiar el valor numérico."""
    print("\n>> EDICION")
    b = input("Cual edito?: ")
    for x in almacen:
        if x["ref"] == b:
            try:
                nuevo = float(input("Nuevo valor: "))
                x["val"] = nuevo
                print("✅ Hecho.")
            except ValueError:
                # Control de errores 2
                print(" Error de formato.")
            return
    print(" Referencia no encontrada.")

def borrar_articulo():
    """Elimina el elemento si coincide la referencia."""
    print("\n>> BORRADO")
    b = input("Cual borro?: ")
    for x in almacen:
        if x["ref"] == b:
            almacen.remove(x)
            print("🗑️ Borrado.")
            return
    print(" No esta en la lista.")

def listar_todo():
    """Vuelca el contenido de la lista."""
    print("\n>> CONTENIDO ACTUAL:")
    if not almacen:
        print("Lista vacia.")
    print("-" * 20)
    for x in almacen:
        # Formato simple sin tablas complejas
        print(f" Ref: {x['ref']} | Val: {x['val']}")
    print("-" * 20)

def ejecutar_menu():
    run = True
    while run:
        # MENÚ VISTOSO HECHO CON CARACTERES
        print("\n" + "█" * 30)
        print("█    CONTROL DE ALMACEN      █")
        print("█" * 30)
        print("█  [1] Nuevo Articulo        █")
        print("█  [2] Buscar Articulo       █")
        print("█  [3] Editar Valor          █")
        print("█  [4] Borrar Articulo       █")
        print("█  [5] Ver Todo              █")
        print("█                            █")
        print("█  [6] Salir                 █")
        print("█" * 30)
        
        op = input("\nElige una opcion > ")

        if op == "1":
            alta_articulo()
        elif op == "2":
            localizar_articulo()
        elif op == "3":
            editar_articulo()
        elif op == "4":
            borrar_articulo()
        elif op == "5":
            listar_todo()
        elif op == "6":
            print("Cerrando sistema...")
            run = False
        else:
            print("Opcion incorrecta.")

if __name__ == "__main__":
    ejecutar_menu()