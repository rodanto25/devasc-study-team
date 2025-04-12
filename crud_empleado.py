# Rodrigo Antonio Estrada Orantes 23270051
# CRUD tabla empleado

import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'oracle',
    'database': 'practica15_23270051'
}

def connect_db():
    return mysql.connector.connect(**config)

# CREAR
def create_empleado(correo, contrasena, puesto):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO empleado (correo, contrasena, puesto) VALUES (%s, %s, %s)",
            (correo, contrasena, puesto)
        )
        conn.commit()
        print("Empleado agregado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# LEER TODOS
def read_empleados():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleado")
        empleados = cursor.fetchall()
        if empleados:
            print("\nLista de Empleados:")
            for emp in empleados:
                print(f"ID: {emp[0]}, Correo: {emp[1]}, Contraseña: {emp[2]}, Puesto: {emp[3]}")
        else:
            print("No hay empleados registrados.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# LEER POR ID
def read_empleado_by_id(id_empleado):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleado WHERE id_empleado = %s", (id_empleado,))
        emp = cursor.fetchone()
        if emp:
            print(f"ID: {emp[0]}, Correo: {emp[1]}, Contraseña: {emp[2]}, Puesto: {emp[3]}")
        else:
            print("Empleado no encontrado.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# ACTUALIZAR
def update_empleado(id_empleado, correo, contrasena, puesto):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE empleado 
               SET correo = %s, contrasena = %s, puesto = %s 
               WHERE id_empleado = %s""",
            (correo, contrasena, puesto, id_empleado)
        )
        conn.commit()
        print("Empleado actualizado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# ELIMINAR
def delete_empleado(id_empleado):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_empleado,))
        conn.commit()
        print("Empleado eliminado.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# MENÚ PRINCIPAL
def main():
    while True:
        print("\n--- CRUD EMPLEADO ---")
        print("1. Agregar empleado")
        print("2. Ver todos los empleados")
        print("3. Buscar empleado por ID")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            correo = input("Correo: ")
            contrasena = input("Contraseña (máx 5 caracteres): ")
            puesto = input("Puesto: ")
            create_empleado(correo, contrasena, puesto)
        elif opcion == '2':
            read_empleados()
        elif opcion == '3':
            id_emp = int(input("ID del empleado: "))
            read_empleado_by_id(id_emp)
        elif opcion == '4':
            id_emp = int(input("ID del empleado a actualizar: "))
            correo = input("Nuevo correo: ")
            contrasena = input("Nueva contraseña (máx 5): ")
            puesto = input("Nuevo puesto: ")
            update_empleado(id_emp, correo, contrasena, puesto)
        elif opcion == '5':
            id_emp = int(input("ID del empleado a eliminar: "))
            delete_empleado(id_emp)
        elif opcion == '6':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
