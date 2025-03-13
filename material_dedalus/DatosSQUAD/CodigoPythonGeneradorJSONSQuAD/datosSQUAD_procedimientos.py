import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"C:\Users\mpord\Documents\3IngSoft\2Cuatri\G4.Dedalus\material_dedalus\DatosSQUAD\resumen_procedimientos.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

pacientes = ["Juan Pérez","María López","Carlos García","Lucía Ramírez","Miguel Rodríguez","Ana Gómez","Pedro Álvarez","Rosa Jiménez","Javier Santos","Alejandro Ruiz"]  


i = 0

for _, row in df.iterrows():
    i+=1
    if(int(row['PacienteID'])-1 < len(pacientes)):
        titulo = f"{pacientes[int(row['PacienteID'])-1]} ID: {row['PacienteID']}"
        nombre = pacientes[int(row['PacienteID'])-1]
    else:
        titulo = f"Paciente {row['PacienteID']} ID: {row['PacienteID']}"
        nombre = "Desconocido"

    context = (
        f"Paciente {row['PacienteID']} nombre {nombre}. "
        f"Procedimientos: {row['Procedimientos']}"
        f"Tratamientos: {row['Tratamientos']}. "
        f"Cirugías Previas: {row['CirugíasPrevias']}. "
        f"Radiologia: {row['Radiologia']}. "
        )

    preguntas = [
        
            {"question": "¿Qué procedimientos se han realizado al paciente?", "id": i, "answers": [{"text": row['Procedimientos'], "answer_start": context.find(str(row['Procedimientos']))}]},
            {"question": "¿Qué tratamientos ha recibido el paciente?", "id": i+1, "answers": [{"text": row['Tratamientos'], "answer_start": context.find(str(row['Tratamientos']))}]},
            {"question": "¿Qué cirugías previas tiene el paciente?", "id": i+2, "answers": [{"text": row['CirugíasPrevias'], "answer_start": context.find(str(row['CirugíasPrevias']))}]},
            {"question": "¿Cuál es el resultado del estudio radiológico del paciente?", "id": i+3, "answers": [{"text": row['Radiologia'], "answer_start": context.find(str(row['Radiologia']))}]} 
        ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=3

# Guardar en JSON
with open("dataset_squad_procedimientos.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
