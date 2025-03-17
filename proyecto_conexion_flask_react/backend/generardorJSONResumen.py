import pandas as pd
import json
import os

# Función para leer varios archivos CSV, filtrar por ID y generar un JSON
def csv_a_json_por_id(csv_files, id_especifico: str):
    # Lista para almacenar los datos filtrados de todos los CSV
    datos_completos = []

    for archivo_csv in csv_files:
        if os.path.exists(archivo_csv):
            # Leer el archivo CSV con pandas
            df = pd.read_csv(archivo_csv)

            try:
                    df['ID'] = df['ID'].astype(type(id_especifico))
            except ValueError:
                print(f"Error al convertir ID en {archivo_csv}. Revisar los datos.")
                continue

            # Comprobar tipo después de la conversión
            print(f"Tipo convertido de ID en {archivo_csv}: {df['ID'].dtype}")
            
            # Filtrar los datos donde la columna 'ID' tenga el valor específico
            datos_filtrados = df[df['ID'] == id_especifico ]
            # print(f"Este es el archivo csv :{archivo_csv}")

            # Convertir NaN a None en todo el DataFrame usando applymap
            datos_filtrados = datos_filtrados.fillna(value="No hay datos")
            #print(f"Datos:{datos_filtrados} \n")


            # Convertir el DataFrame filtrado a un diccionario
            if not datos_filtrados.empty:
                datos_completos.append(datos_filtrados.to_dict(orient='records'))  # 'records' crea una lista de diccionarios
        else:
            print(f"El archivo {archivo_csv} no existe.")

    # Si se encontraron datos, guardarlos en el archivo JSON
    if datos_completos:
        # print(datos_completos)
        return datos_completos
    