import json
import requests
from typing import TextIO
import time

# Cargar el archivo JSON SQuAD
with open("datos_pacientes/dataset_squad_procedimientos.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Lista para almacenar los embeddings
embeddings_data = {}

# Configurar la cabecera para la API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer sk-lqIaTaCA6djhkYLWFx5Gww"
}

# Recorrer los datos y generar embeddings
for entry in data["data"]:
    patient_id = entry["title"].strip()

    if patient_id not in embeddings_data:
        embeddings_data[patient_id] = []  # Inicializar lista para este paciente

    for paragraph in entry["paragraphs"]:
        context = paragraph["context"]
        for qa in paragraph["qas"]:
            question = qa["question"]
            answer = qa["answers"][0]["text"]  # Tomamos la primera respuesta

            payload = {
                "model": "bedrock/amazon.titan-embed-text-v2:0",
                "input": f"{context} {question}"
            }

            response = requests.post(
                "https://litellm.dccp.pbu.dedalus.com/embeddings",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                embeddings_data[patient_id].append({
                    "context": context,
                    "question": question,
                    "answer": answer,
                    "embedding": result
                })
            else :
                print(f"Error al generar embeddings para el paciente {patient_id}")
                print(response.json())

            time.sleep(2)

# Guardar los embeddings en un archivo JSON
with open("embeddings.json", "w", encoding="utf-8") as file:
    json.dump(embeddings_data, file, ensure_ascii=False, indent=4)

print("Embeddings generados y guardados en embeddings.json")

# EMBEDDINGS QUE VAN BIEN:

# import json
# import requests
#
# text = "hola esto es una preuba de embeddings"
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer sk-lqIaTaCA6djhkYLWFx5Gww"
# }
#
# payload = {
#     "model": "bedrock/amazon.titan-embed-text-v2:0",
#     "input": text
# }
#
# response = requests.post(
#     "https://litellm.dccp.pbu.dedalus.com/embeddings",
#     headers=headers,
#     json=payload
# )
#
# if response.status_code == 200:
#     result = response.json()
#
# print(result)

