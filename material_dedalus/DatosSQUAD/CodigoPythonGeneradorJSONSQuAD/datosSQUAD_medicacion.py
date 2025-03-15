import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"CSV\resumen_medicacion.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

pacientes = ["Juan Pérez","María López","Carlos García","Lucía Ramírez","Miguel Rodríguez","Ana Gómez","Pedro Álvarez","Rosa Jiménez","Javier Santos","Alejandro Ruiz"]  


i = 0

for _, row in df.iterrows():
    i+=1
    titulo = f"{row['ID']}"
    context = (
        f"Paciente {row['ID']} nombre {pacientes[int(row['ID'])-1]}. "
        f"Medicamento: {row['Medicamento']} Dosis: {row['Dosis']}. "
        f"Via: {row['Via']}. "
        )

    preguntas = [
            {"question": "¿Qué medicamento está recibiendo el paciente?", "id": i, "answers": [{"text": row['Medicamento'], "answer_start": context.find(str(row['Medicamento']))}]},
            {"question": "¿Cuál es la dosis del medicamento?", "id": i+1, "answers": [{"text": row['Dosis'], "answer_start": context.find(str(row['Dosis']))}]},
            {"question": "¿Cuál es la vía de administración del medicamento?", "id": i+2, "answers": [{"text": row['Via'], "answer_start": context.find(str(row['Via']))}]} 
        
            ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=2

# Guardar en JSON
with open("dataset_squad_medicion.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
