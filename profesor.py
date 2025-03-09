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

# 🔹 CREAR Profesor
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

# 🔹 LEER Todos los Profesores
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

# 🔹 LEER Profesor por Clave
def read_profesor_by_clave(clave_prof):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profesor WHERE clave_prof = %s", (clave_prof,))
        result = cursor.fetchone()
        if result:
            print(f"Clave: {result[0]}, Nombre: {result[1]}, Rubrica ID: {result[2]}, Área Conocimiento ID: {result[3]}")
        else:
            print(f"No se encontró el profesor con clave: {clave_prof}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# 🔹 ACTUALIZAR Profesor
def update_profesor(clave_prof, nuevo_nombre_prof, nueva_rubrica_id, nueva_rubrica_area_conocimiento_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE profesor SET nombre_prof = %s, rubrica_id = %s, rubrica_area_conocimiento_id = %s WHERE clave_prof = %s",
            (nuevo_nombre_prof, nueva_rubrica_id, nueva_rubrica_area_conocimiento_id, clave_prof)
        )
        conn.commit()
        print(f"Profesor con clave '{clave_prof}' actualizado a '{nuevo_nombre_prof}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# 🔹 ELIMINAR Profesor
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
