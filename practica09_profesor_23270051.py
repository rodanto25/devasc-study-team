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
def create_profesor(clave_prof, nombre_prof, rubrica_id, rubrica_area_conocimiento_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profesor (clave_prof, nombre_prof, rubrica_id, rubrica_area_conocimiento_id) VALUES (%s, %s, %s, %s)", 
            (clave_prof, nombre_prof, rubrica_id, rubrica_area_conocimiento_id)
        )
        conn.commit()
        print(f"Profesor '{nombre_prof}' agregado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  LEER 
def read_profesores():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profesor")
        result = cursor.fetchall()
        for row in result:
            print(f"Clave: {row[0]}, Nombre: {row[1]}, Rubrica ID: {row[2]}, Área Conocimiento ID: {row[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
def read_profesor_by_clave(clave_prof):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profesor WHERE clave_prof = %s", (clave_prof,))
        result = cursor.fetchone()
        if result:
            print("\nlista de Profesores:")
            for row in result:
                print(f"Clave: {row[0]}, Nombre: {row[1]}, Rubrica ID: {row[2]}, Área Conocimiento ID: {row[3]}")
        else:
            print("no hay profesores registrados.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  ACTUALIZAR 
def update_profesor(clave_prof, nuevo_nombre_prof, nueva_rubrica_id, nueva_rubrica_area_conocimiento_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE profesor SET nombre_prof = %s, rubrica_id = %s, rubrica_area_conocimiento_id = %s WHERE clave_prof = %s",
            (nuevo_nombre_prof, nueva_rubrica_id, nueva_rubrica_area_conocimiento_id, clave_prof)
        )
        conn.commit()
        print(f"Profesor con clave '{clave_prof}' actualizado a '{nuevo_nombre_prof}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

#  ELIMINAR 
def delete_profesor(clave_prof):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profesor WHERE clave_prof = %s", (clave_prof,))
        conn.commit()
        print(f"Profesor con clave '{clave_prof}' eliminado.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
#  MENU
def main():
    while True:
        print("\n--- menu CRUD de profesor ---")
        print("1. agregar profesor")
        print("2. mostrar todos los profesores")
        print("3. buscar profesor por clave")
        print("4. actualizar profesor")
        print("5. eliminar profesor")
        print("6. salir")

        opcion = input("seleccionar una opción (1-6): ")

        if opcion == '1':
            clave = input("ingrese la clave del profesor: ")
            nombre = input("ingrese el nombre del profesor: ")
            rubrica_id = input("ingrese el ID de la rubrica: ")
            area_conocimiento_id = input("ingrese el ID del area de conocimiento: ")
            create_profesor(clave, nombre, rubrica_id, area_conocimiento_id)
        elif opcion == '2':
            read_profesores()
        elif opcion == '3':
            clave = input("ingrese la clave del profesor a buscar: ")
            read_profesor_by_clave(clave)
        elif opcion == '4':
            clave = input("ingrese la clave del profesor a actualizar: ")
            nuevo_nombre = input("ingrese el nuevo nombre del profesor: ")
            nueva_rubrica_id = input("ingrese el nuevo ID de la rúbrica: ")
            nueva_area_conocimiento_id = input("ingrese el nuevo ID del área de conocimiento: ")
            update_profesor(clave, nuevo_nombre, nueva_rubrica_id, nueva_area_conocimiento_id)
        elif opcion == '5':
            clave = input("ingrese la clave del profesor a eliminar: ")
            delete_profesor(clave)
        elif opcion == '6':
            print("adios")
            break
        else:
            print("intente de nuevo")

#  MAIN
if __name__ == "__main__":
    main()