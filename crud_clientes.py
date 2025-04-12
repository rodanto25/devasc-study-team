# Rodrigo Antonio Estrada Orantes 23270051
# CRUD tabla clientes

import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'oracle',
    'database': 'practica15_23270051'
}

def conectar():
    return mysql.connector.connect(**config)

# crear nuevo cliente
def agregar_cliente():
    nombre = input("Nombre del cliente: ")
    telefono = input("Teléfono: ")

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)", (nombre, telefono))
        conn.commit()
        print("cliente agregado correctamente.")
    except mysql.connector.Error as err:
        print(f"error: {err}")
    finally:
        cursor.close()
        conn.close()

# leer todos los clientes
def mostrar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    print("\nlista de Clientes:")
    for c in clientes:
        print(f"ID: {c[0]} | Nombre: {c[1]} | Teléfono: {c[2]}")
    cursor.close()
    conn.close()

# buscar cliente por ID
def buscar_cliente():
    try:
        id_cliente = int(input("ID del cliente a buscar: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        c = cursor.fetchone()
        if c:
            print(f"ID: {c[0]} | Nombre: {c[1]} | Teléfono: {c[2]}")
        else:
            print("cliente no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# actualizar cliente
def actualizar_cliente():
    try:
        id_cliente = int(input("ID del cliente a actualizar: "))
        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_telefono = input("Nuevo teléfono: ")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes SET nombre = %s, telefono = %s WHERE id_cliente = %s
        """, (nuevo_nombre, nuevo_telefono, id_cliente))
        conn.commit()

        if cursor.rowcount > 0:
            print("cliente actualizado correctamente.")
        else:
            print("cliente no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# Eliminar cliente
def eliminar_cliente():
    try:
        id_cliente = int(input("ID del cliente a eliminar: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()

        if cursor.rowcount > 0:
            print("cliente eliminado correctamente.")
        else:
            print("cliente no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# Menu principal
def menu():
    while True:
        print("\n--- Menu CRUD Clientes ---")
        print("1. Agregar cliente")
        print("2. Mostrar todos los clientes")
        print("3. Buscar cliente por ID")
        print("4. Actualizar cliente")
        print("5. Eliminar cliente")
        print("6. Salir")

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            agregar_cliente()
        elif opcion == '2':
            mostrar_clientes()
        elif opcion == '3':
            buscar_cliente()
        elif opcion == '4':
            actualizar_cliente()
        elif opcion == '5':
            eliminar_cliente()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("opción no válida.")

# Ejecutar
if __name__ == "__main__":
    menu()