import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"CSV\resumen_lab_iniciales_conNombre.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

i = 0

for _, row in df.iterrows():
    i+=1
    titulo = f"{row['ID']}"
    context = (
        f"Paciente {row['ID']} nombre {row['Nombre']}. "
            f"Glucosa: {row['Glucosa']} mg/dL. "
            f"pH: {row['pH']}. "
            f"Cetonas: {row['Cetonas']} mmol/L. "
            f"Creatinina: {row['Creatinina']} mg/dL. "
            f"Hemoglobina: {row['Hemoglobina']} g/dL. "
            f"Leucocitos: {row['Leucocitos']} células/mm³. "
            f"Sodio: {row['Sodio']} mEq/L. "
            f"Potasio: {row['Potasio']} mEq/L. "
            f"Urea: {row['Urea']} mg/dL. "
            f"Amilasa: {row['Amilasa']} U/L. "
    )

    preguntas = [
            {"question": "¿Cuál es el nivel de glucosa del paciente?", "id": i, "answers": [{"text": row['Glucosa'], "answer_start": context.find(str(row['Glucosa']))}]},
            {"question": "¿Cuál es el pH del paciente?", "id": i+1, "answers": [{"text": row['pH'], "answer_start": context.find(str(row['pH']))}]},
            {"question": "¿Cuál es el nivel de cetonas del paciente?", "id": i+2, "answers": [{"text": row['Cetonas'], "answer_start": context.find(str(row['Cetonas']))}]},
            {"question": "¿Cuál es el nivel de creatinina del paciente?", "id": i+3, "answers": [{"text": row['Creatinina'], "answer_start": context.find(str(row['Creatinina']))}]},
            {"question": "¿Cuál es el nivel de hemoglobina del paciente?", "id": i+4, "answers": [{"text": row['Hemoglobina'], "answer_start": context.find(str(row['Hemoglobina']))}]},
            {"question": "¿Cuántos leucocitos tiene el paciente?", "id": i+5, "answers": [{"text": row['Leucocitos'], "answer_start": context.find(str(row['Leucocitos']))}]},
            {"question": "¿Cuál es el nivel de sodio del paciente?", "id": i+6, "answers": [{"text": row['Sodio'], "answer_start": context.find(str(row['Sodio']))}]},
            {"question": "¿Cuál es el nivel de potasio del paciente?", "id": i+7, "answers": [{"text": row['Potasio'], "answer_start": context.find(str(row['Potasio']))}]},
            {"question": "¿Cuál es el nivel de urea del paciente?", "id": i+8, "answers": [{"text": row['Urea'], "answer_start": context.find(str(row['Urea']))}]},
            {"question": "¿Cuál es el nivel de amilasa del paciente?", "id": i+9, "answers": [{"text": row['Amilasa'], "answer_start": context.find(str(row['Amilasa']))}]}
        ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=9

# Guardar en JSON
with open("dataset_squad_lab_iniciales.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
