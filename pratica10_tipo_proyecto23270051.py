#Rodrigo Antonio Estrada Orantes 23270051
# https://github.com/rodanto25/devasc-study-team.git
import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'oracle',
    'database': 'db_taller23270051'
}

def connect_db():
    """Establece conexión con la base de datos."""
    return mysql.connector.connect(**config)

#  CREAR 
def create_tipo(tipo, nombre_tipo):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tipo_proyecto (tipo, nombre_tipo) VALUES (%s, %s)", (tipo, nombre_tipo))
        conn.commit()
        print(f"Tipo de proyecto '{nombre_tipo}' agregado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  LEER 
def read_tipos():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_proyecto")
        result = cursor.fetchall()
        if result:
            print("\nlista de Tipos de Proyecto:")
            for row in result:
                print(f"tipo: {row[0]}, nombre: {row[1]}")
        else:
            print("no hay tipos de proyecto registrados.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
def read_tipo_by_clave(tipo):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_proyecto WHERE tipo = %s", (tipo,))
        result = cursor.fetchone()
        if result:
            print(f"Tipo: {result[0]}, nombre: {result[1]}")
        else:
            print(f"No se encontró el tipo de proyecto con clave: {tipo}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  ACTUALIZAR
def update_tipo(tipo, nuevo_nombre_tipo):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE tipo_proyecto SET nombre_tipo = %s WHERE tipo = %s", (nuevo_nombre_tipo, tipo))
        conn.commit()
        print(f"Tipo de proyecto con clave '{tipo}' actualizado a '{nuevo_nombre_tipo}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  ELIMINAR 
def delete_tipo(tipo):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo_proyecto WHERE tipo = %s", (tipo,))
        conn.commit()
        print(f"Tipo de proyecto con clave '{tipo}' eliminado.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
#  MENU
def main():
    while True:
        print("\n--- menu CRUD de tipos de proyectos ---")
        print("1. agregar tipo de proyecto")
        print("2. mostrar todos los tipos de proyecto")
        print("3. buscar tipo de proyecto por clave")
        print("4. actualizar tipo de proyecto")
        print("5. eliminar tipo de proyecto")
        print("6. salir")

        opcion = input("seleccionar una opción (1-6): ")

        if opcion == '1':
            tipo = input("ingrese la clave del tipo de proyecto: ")
            nombre = input("ingrese el nombre del tipo de proyecto: ")
            create_tipo(tipo, nombre)
        elif opcion == '2':
            read_tipos()
        elif opcion == '3':
            tipo = input("ingrese la clave del tipo de proyecto a buscar: ")
            read_tipo_by_clave(tipo)
        elif opcion == '4':
            tipo = input("ingrese la clave del tipo de proyecto a actualizar: ")
            nuevo_nombre = input("ingrese el nuevo nombre del tipo de proyecto: ")
            update_tipo(tipo, nuevo_nombre)
        elif opcion == '5':
            tipo = input("ingrese la clave del tipo de proyecto a eliminar: ")
            delete_tipo(tipo)
        elif opcion == '6':
            print("adios")
            break
        else:
            print("no es valido intente de nuevo")

#  MAIN
if __name__ == "__main__":
    main()