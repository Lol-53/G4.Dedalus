import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"CSV\resumen_notas_fechaEstandar.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

pacientes = ["Juan Pérez","María López","Carlos García","Lucía Ramírez","Miguel Rodríguez","Ana Gómez","Pedro Álvarez","Rosa Jiménez","Javier Santos","Alejandro Ruiz"]  


i = 0

for _, row in df.iterrows():
    i+=1
    if(int(row['ID'])-1 < len(pacientes)):
        titulo = f"{row['ID']}"
        nombre = pacientes[int(row['ID'])-1]
    else:
        continue
    context = (
        f"Paciente {row['ID']} nombre {nombre}. "
        f"Fecha: {row['Fecha']}"
        f"Nota médica: {row['Nota']}. "
        )

    preguntas = [
            {"question": "¿Qué información hay en la nota médica?", "id": i, "answers": [{"text": row['Nota'], "answer_start": context.find(str(row['Nota']))}]},
            ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=2

# Guardar en JSON
with open("dataset_squad_notas.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
