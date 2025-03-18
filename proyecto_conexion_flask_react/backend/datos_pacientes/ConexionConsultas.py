import mysql.connector
import csv


config={
    "user":'root',
    'password':'MariaBD_Root',
    'host':'localhost',
    'database':'dedalus'
}

def conectar():
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as a:
        return ('Error al conectar a mariadb',a)  # o podemos devolver False

def cerrar_conexion(conexion):
    if conexion in locals():
        conexion.close()
        print('Conexion cerrada')
        return True


def consultar_todos_pacientes(conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM paciente "
    cursor.execute(consulta_query)
    datos = cursor.fetchall()
    return datos

def consultar_Chat(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT Historial FROM chat WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    return datos

def consultar_datos_paciente(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM paciente WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    return datos

def consultar_evolucion(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM evolucion WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    datos = quitarID(datos)
    return datos

def consultar_lab_iniciales(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM lab_iniciales WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    datos = quitarID(datos)
    return datos

def consultar_medicacion(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM medicacion WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    datos = quitarID(datos)
    return datos

def consultar_notas(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM notas WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    datos = quitarID(datos)
    return datos

def consultar_procedimiento(ID,conexion):
    cursor = conexion.cursor()
    consulta_query = "SELECT * FROM procedimiento WHERE ID = %s"
    cursor.execute(consulta_query,(ID,))
    datos = cursor.fetchall()
    datos = quitarID(datos)
    return datos

def quitarID(Datos):
    return [fila[1:] for fila in Datos]


def insertar_datos_csv(file_name, tabla_name, conexion):
    cursor= conexion.cursor()
    with open(file_name, newline='',encoding='utf-8') as csvfile:
        lector_csv = csv.reader(csvfile)

        columnas = next(lector_csv)

        placeholders = ", ".join(["%s"]* len(columnas)) 
        consulta = f"INSERT INTO {tabla_name} ({', '.join(columnas)}) VALUES ({placeholders})"
        
        for fila in lector_csv:
            cursor.execute(consulta, tuple(fila))
        
    conexion.commit()

def exportar_csv_tabla (file_name,tabla_name,conexion):
    cursor = conexion.cursor()

    cursor.execute(f"SELECT * FROM {tabla_name}")
    filas= cursor.fetchall()

    columnas = [i[0] for i in cursor.description]  # Obtener nombres de columnas

    with open(file_name, mode='w', newline='', encoding='utf-8') as f:
            escritor_csv = csv.writer(f)
            escritor_csv.writerow(columnas)  # Escribir encabezado
            escritor_csv.writerows(filas)   # Escribir datos


conexion=conectar()
exportar_csv_tabla("datos_pacientes/info_pacientes.csv", "paciente", conexion)
exportar_csv_tabla("datos_pacientes/notas.csv", "notas", conexion)
exportar_csv_tabla("datos_pacientes/resumen_evolucion_process.csv", "evolucion", conexion)
exportar_csv_tabla("datos_pacientes/resumen_lab_iniciales.csv", "lab_iniciales", conexion)
exportar_csv_tabla("datos_pacientes/resumen_medicacion.csv", "medicacion", conexion)
exportar_csv_tabla("datos_pacientes/resumen_procedimientos.csv", "procedimiento", conexion)
cerrar_conexion(conexion)


