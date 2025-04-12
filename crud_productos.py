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

def agregar_producto():
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))
    id_proveedor = input("ID del proveedor (puede estar vacío): ")
    id_proveedor = int(id_proveedor) if id_proveedor else None

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, descripcion, precio, stock, id_proveedor) VALUES (%s, %s, %s, %s, %s)",
                   (nombre, descripcion, precio, stock, id_proveedor))
    conn.commit()
    cursor.close()
    conn.close()
    print("producto agregado correctamente.")

def mostrar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    for producto in cursor.fetchall():
        print(producto)
    cursor.close()
    conn.close()

def buscar_producto_por_id():
    id_producto = int(input("ID del producto a buscar: "))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    if producto:
        print(producto)
    else:
        print("producto no encontrado.")
    cursor.close()
    conn.close()

def actualizar_producto():
    id_producto = int(input("ID del producto a actualizar: "))
    nombre = input("Nuevo nombre: ")
    descripcion = input("Nueva descripción: ")
    precio = float(input("Nuevo precio: "))
    stock = int(input("Nuevo stock: "))
    id_proveedor = input("Nuevo ID del proveedor (puede estar vacío): ")
    id_proveedor = int(id_proveedor) if id_proveedor else None

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos 
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, id_proveedor=%s 
        WHERE id_producto=%s
    """, (nombre, descripcion, precio, stock, id_proveedor, id_producto))
    conn.commit()
    cursor.close()
    conn.close()
    print("producto actualizado.")

def eliminar_producto():
    id_producto = int(input("ID del producto a eliminar: "))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    print("producto eliminado.")

def menu():
    while True:
        print("\n--- Menú CRUD de Productos ---")
        print("1. Agregar producto")
        print("2. Mostrar todos los productos")
        print("3. Buscar producto por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            mostrar_productos()
        elif opcion == '3':
            buscar_producto_por_id()
        elif opcion == '4':
            actualizar_producto()
        elif opcion == '5':
            eliminar_producto()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("opción no valida.")

if __name__ == "__main__":
    menu()