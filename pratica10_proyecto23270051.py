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

# 🔹 CREAR 
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

# 🔹 LEER 
def read_tipos():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_proyecto")
        result = cursor.fetchall()
        for row in result:
            print(f"Tipo: {row[0]}, Nombre: {row[1]}")
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
            print(f"Tipo: {result[0]}, Nombre: {result[1]}")
        else:
            print(f"No se encontró el tipo de proyecto con clave: {tipo}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# 🔹 ACTUALIZAR
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

# 🔹 ELIMINAR 
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