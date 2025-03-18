import pandas as pd
def obtenerDiagnostico(path_CSV_pacientes:str,ID:str):
    try:
        df = pd.read_csv(path_CSV_pacientes)

        datos_id = df[df["ID"]==ID]

        return datos_id['DiagnosticoPrincipal'][1]
    except ValueError:
        return "No se encontro diagnóstico"  
    

