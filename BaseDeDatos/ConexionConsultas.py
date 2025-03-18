import mariadb
from flask import Flask, jsonify

app = Flask(__name__)

# Configuración de la conexión a MariaDB
def get_db_connection():
    try:
        conn = mariadb.connect(
            host="localhost",  # O la IP del servidor
            user="tu_usuario",
            password="tu_contraseña",
            database="nombre_de_la_base_de_datos"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def extraer_csv (name_table:str):
    path_csv="No se pudo obtener el csv"
    conn = get_db_connection()
    if conn is None:
        return print("Error: No se pudo conectar a la base de datos")
    
    try:
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM ?",(name_table,))

    except mariadb.Error as e:
        print(f"Error al importar datos: {e}")
    finally:
        cursor.close()
        conn.close()

def importar_datos_txt(file_name_path:str):

    conn = get_db_connection()
    if conn is None:
        return print("Error: No se pudo conectar a la base de datos")
               
    try:
        cursor = conn.cursor()
        query = f"""
                LOAD DATA LOCAL INFILE '{file_name_path}'
                INTO TABLE mi_tabla
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"' 
                LINES TERMINATED BY '\n';
            """
        cursor.execute(query)
        conn.commit()

    except mariadb.Error as e:
        print(f"Error al importar datos: {e}")
    finally:
        cursor.close()
        conn.close()

    """CUIDADO!!
    La base de datos debe de tener habilitado:
    Debe estar habilitada la opción local-infile=1 en la configuración de MariaDB.
    Para aceptar subir valores desde un cliente local
    """


@app.route('/users')
def get_users():
    conn = get_db_connection()
    if conn is None:
        return print("Error: No se pudo conectar a la base de datos")
    
    cursor = conn.cursor(dictionary=True)  # Devuelve los resultados como diccionarios
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
