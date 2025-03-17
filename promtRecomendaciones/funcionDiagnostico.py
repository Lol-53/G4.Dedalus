import pandas as pd
def obtenerDiagnostico(path_CSV_pacientes:str,ID:str):

    diagnostico= "No se encontro diagnóstico"
    df = pd.read_csv(path_CSV_pacientes)
    print(df.columns)

    datos_id = df[df["ID"]==ID]



    print(datos_id)

    return datos_id['DiagnosticoPrincipal'][1]

