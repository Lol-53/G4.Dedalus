import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"C:\Users\mpord\Documents\3IngSoft\2Cuatri\G4.Dedalus\material_dedalus\DataSetIndividuales\resumen_pacientes.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

for _, row in df.iterrows():
    contexto = (
        f"Paciente {row['Nombre']} de {row['Edad']} años, {row['Sexo']}. "
        f"Alergias: {row['Alergias']}. Motivo de ingreso: {row['MotivoIngreso']}. "
        f"Diagnóstico principal: {row['DiagnosticoPrincipal']}. "
        f"Condiciones previas: {row['CondicionesPrevias']}. "
        f"Fecha de ingreso: {row['FechaIngreso']}. Servicio: {row['Servicio']}. "
        f"Estado al ingreso: {row['EstadoAlIngreso']}."
    )

    preguntas = [
        {"question": "¿Cuál es el motivo de ingreso?", "answers": [{"text": row["MotivoIngreso"], "answer_start": contexto.find(row["MotivoIngreso"])}]},
        {"question": "¿Cuál es el diagnóstico principal?", "answers": [{"text": str(row["DiagnosticoPrincipal"]), "answer_start": contexto.find(str(row["DiagnosticoPrincipal"]))}]},
        {"question": "¿Tiene alergias?", "answers": [{"text": row["Alergias"], "answer_start": contexto.find(row["Alergias"])}]},
    ]

    data["data"].append({"title": row["Nombre"], "paragraphs": [{"context": contexto, "qas": preguntas}]})

# Guardar en JSON
with open("dataset_squad.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
