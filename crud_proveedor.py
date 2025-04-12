# Rodrigo Antonio Estrada Orantes 23270051
# CRUD tabla proveedor

import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'oracle',
    'database': 'practica15_23270051'
}

def conectar():
    return mysql.connector.connect(**config)

# Crear un nuevo proveedor
def agregar_proveedor():
    nombre = input("Nombre del proveedor: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    correo = input("Correo: ")

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO proveedor (nombre, telefono, direccion, correo) VALUES (%s, %s, %s, %s)",
                       (nombre, telefono, direccion, correo))
        conn.commit()
        print("Proveedor agregado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Mostrar todos los proveedores
def mostrar_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedor")
    proveedores = cursor.fetchall()
    print("\n--- Lista de Proveedores ---")
    for p in proveedores:
        print(f"ID: {p[0]}, Nombre: {p[1]}, Tel: {p[2]}, Dirección: {p[3]}, Correo: {p[4]}")
    cursor.close()
    conn.close()

# Buscar proveedor por ID
def buscar_proveedor():
    try:
        id_buscar = int(input("ID del proveedor a buscar: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_buscar,))
        p = cursor.fetchone()
        if p:
            print(f"ID: {p[0]}, Nombre: {p[1]}, Tel: {p[2]}, Dirección: {p[3]}, Correo: {p[4]}")
        else:
            print("Proveedor no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# Actualizar proveedor
def actualizar_proveedor():
    try:
        id_proveedor = int(input("ID del proveedor a actualizar: "))
        nombre = input("Nuevo nombre: ")
        telefono = input("Nuevo teléfono: ")
        direccion = input("Nueva dirección: ")
        correo = input("Nuevo correo: ")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proveedor 
            SET nombre = %s, telefono = %s, direccion = %s, correo = %s 
            WHERE id_proveedor = %s
        """, (nombre, telefono, direccion, correo, id_proveedor))
        conn.commit()
        if cursor.rowcount > 0:
            print("Proveedor actualizado correctamente.")
        else:
            print("Proveedor no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# Eliminar proveedor
def eliminar_proveedor():
    try:
        id_proveedor = int(input("ID del proveedor a eliminar: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Proveedor eliminado correctamente.")
        else:
            print("Proveedor no encontrado.")
        cursor.close()
        conn.close()
    except ValueError:
        print("ID inválido.")

# Menú principal
def menu():
    while True:
        print("\n--- CRUD Proveedor ---")
        print("1. Agregar proveedor")
        print("2. Mostrar todos los proveedores")
        print("3. Buscar proveedor por ID")
        print("4. Actualizar proveedor")
        print("5. Eliminar proveedor")
        print("6. Salir")

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            agregar_proveedor()
        elif opcion == '2':
            mostrar_proveedores()
        elif opcion == '3':
            buscar_proveedor()
        elif opcion == '4':
            actualizar_proveedor()
        elif opcion == '5':
            eliminar_proveedor()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

# Ejecutar
if __name__ == "__main__":
    menu()