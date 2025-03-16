import pandas as pd
import json
import os

# Función para leer varios archivos CSV y generar un JSON
def csv_a_json(csv_files, output_json):
    # Lista para almacenar los datos de todos los CSV
    datos_completos = []

    for archivo_csv in csv_files:
        if os.path.exists(archivo_csv):
            # Leer el archivo CSV con pandas
            df = pd.read_csv(archivo_csv)
            
            # Convertir el DataFrame a un diccionario
            datos_completos.append(df.to_dict(orient='records'))  # 'records' crea una lista de diccionarios
        else:
            print(f"El archivo {archivo_csv} no existe.")
    
    # Guardar los datos combinados en un archivo JSON
    with open(output_json, 'w') as json_file:
        json.dump(datos_completos, json_file, indent=4)
        print(f"Archivo JSON generado: {output_json}")

# Lista de archivos CSV a leer
archivos_csv = [""]

# Llamada a la función para generar el JSON
csv_a_json(archivos_csv, "resultado.json")
