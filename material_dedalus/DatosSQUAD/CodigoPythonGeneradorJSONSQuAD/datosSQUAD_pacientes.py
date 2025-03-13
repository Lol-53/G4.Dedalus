import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"C:\Users\mpord\Documents\3IngSoft\2Cuatri\G4.Dedalus\material_dedalus\DatosSQUAD\resumen_pacientes.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

i = 0

for _, row in df.iterrows():
    i+=1
    titulo = f"{row['Nombre']} ID: {row['PacienteID']}"

    context = (
        f"Paciente {row['Nombre']} de {row['Edad']} años, {row['Sexo']}. "
        f"Alergias: {row['Alergias']}. Motivo de ingreso: {row['MotivoIngreso']}. "
        f"Diagnóstico principal: {row['DiagnosticoPrincipal']}. "
        f"Condiciones previas: {row['CondicionesPrevias']}. "
        f"Fecha de ingreso: {row['FechaIngreso']}. Servicio: {row['Servicio']}. "
        f"Estado al ingreso: {row['EstadoAlIngreso']}."
        )

    preguntas = [
            {"question": "¿Qué edad tiene el paciente?", "id": i, "answers": [{"text": row['Edad'], "answer_start": context.find(str(row['Edad']))}]},
            {"question": "¿Cuál es el sexo del paciente?", "id": i+1, "answers": [{"text": row['Sexo'], "answer_start": context.find(str(row['Sexo']))}]},
            {"question": "¿El paciente tiene alergias?", "id": i+2, "answers": [{"text": row['Alergias'], "answer_start": context.find(row['Alergias'])}]},
            {"question": "¿Cuál es el motivo de ingreso del paciente?", "id": i+3, "answers": [{"text": row['MotivoIngreso'], "answer_start": context.find(str(row['MotivoIngreso']))}]},
            {"question": "¿Cuál es el diagnóstico principal del paciente?", "id": i+4, "answers": [{"text": row['DiagnosticoPrincipal'], "answer_start": context.find(str(row['DiagnosticoPrincipal']))}]},
            {"question": "¿Qué condiciones previas tiene el paciente?", "id": i+5, "answers": [{"text": row['CondicionesPrevias'], "answer_start": context.find(str(row['CondicionesPrevias']))}]},
            {"question": "¿En qué fecha ingresó el paciente?", "id": i+6, "answers": [{"text": row['FechaIngreso'], "answer_start": context.find(str(row['FechaIngreso']))}]},
            {"question": "¿En qué servicio fue ingresado el paciente?", "id": i+7, "answers": [{"text": row['Servicio'], "answer_start": context.find(str(row['Servicio']))}]},
            {"question": "¿Cuál era el estado del paciente al ingreso?", "id": i+8, "answers": [{"text": row['EstadoAlIngreso'], "answer_start": context.find(str(row['EstadoAlIngreso']))}]}
        ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=8

# Guardar en JSON
with open("dataset_squad_pacientes.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
