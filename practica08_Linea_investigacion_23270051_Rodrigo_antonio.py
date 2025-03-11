#Rodrigo Antonio Estrada Orantes 23270051
import mysql.connector

config = {
    'host': 'localhost',  
    'user': 'root',  
    'password': 'oracle',  
    'database': 'db_taller23270051'  
}

def connect_db():
    return mysql.connector.connect(**config)

# Crear
def create_linea(clave_linea, nombre_linea):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO linea_investigacion (clave_linea, nombre_linea) VALUES (%s, %s)", (clave_linea, nombre_linea))
        conn.commit()
        print(f"Línea de investigación '{nombre_linea}' agregada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Leer
def read_lineas():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM linea_investigacion")
        result = cursor.fetchall()
        for row in result:
            print(f"Clave: {row[0]}, Nombre: {row[1]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def read_linea_by_clave(clave_linea):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM linea_investigacion WHERE clave_linea = %s", (clave_linea,))
        result = cursor.fetchone()
        if result:
            print(f"Clave: {result[0]}, Nombre: {result[1]}")
        else:
            print(f"No se encontró la línea con clave: {clave_linea}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Actualizar
def update_linea(clave_linea, nuevo_nombre_linea):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE linea_investigacion SET nombre_linea = %s WHERE clave_linea = %s", (nuevo_nombre_linea, clave_linea))
        conn.commit()
        print(f"Línea de investigación con clave '{clave_linea}' actualizada a '{nuevo_nombre_linea}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Eliminar
def delete_linea(clave_linea):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM linea_investigacion WHERE clave_linea = %s", (clave_linea,))
        conn.commit()
        print(f"Línea de investigación con clave '{clave_linea}' eliminada.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()