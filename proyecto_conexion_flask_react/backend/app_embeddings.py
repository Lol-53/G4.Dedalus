from flask import Flask, request, jsonify
import openai  # Utiliza el proxy de litellm
import pandas as pd
from flask_cors import CORS
import numpy as np
import requests
import json

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas de Flask

# Cargar embeddings
with open("embeddings/embeddings_evolucion.json", "r", encoding="utf-8") as file:
    embeddings_evolucion = json.load(file)
with open("embeddings/embeddings_lab_iniciales.json", "r", encoding="utf-8") as file:
    embeddings_lab_iniciales = json.load(file)
with open("embeddings/embeddings_medicion.json", "r", encoding="utf-8") as file:
    embeddings_medicion= json.load(file)
with open("embeddings/embeddings_notas.json", "r", encoding="utf-8") as file:
    embeddings_notas = json.load(file)
with open("embeddings/embeddings_procedimientos.json", "r", encoding="utf-8") as file:
    embeddings_procedimientos = json.load(file)

embeddingFiles = [embeddings_evolucion, embeddings_lab_iniciales, embeddings_medicion, embeddings_notas, embeddings_procedimientos]

all_embeddings = []

for emb in embeddingFiles:
    for key, value in emb.items():  # Acceder a la clave y el valor
        for item in value:  # La lista contenida en cada clave
            # Añadir cada elemento de la lista de forma que se preserve la clave
            item["key"] = key  # Agregar la clave como un campo adicional en cada diccionario
            all_embeddings.append(item)

# Función para calcular la similitud coseno entre dos vectores
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
    base_url="https://litellm.dccp.pbu.dedalus.com"
)

# Cargar datos de pacientes (solo una vez al iniciar)
info_pacientes_df = pd.read_csv("datos_pacientes/info_pacientes.csv")
notas_df = pd.read_csv("datos_pacientes/notas.csv")

# Almacenar contexto de pacientes en memoria
contextos_pacientes = {}

conversation_history = {}

def generarEmbedding(user_message, id_paciente):

    user_embedding = None
    embeddings = {"role": "system", "content": "información relevante ofrecida en formato json SQUaD: "}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer sk-lqIaTaCA6djhkYLWFx5Gww"
    }

    payload = {
        "model": "bedrock/amazon.titan-embed-text-v2:0",
        "input": user_message
    }

    response = requests.post(
        "https://litellm.dccp.pbu.dedalus.com/embeddings",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        response_json = response.json()
        user_embedding = response_json["data"][0]["embedding"]

    if(user_embedding):
        best_match = None
        best_score = -1
        second_best_match = None
        second_best_score = -1

        for item in all_embeddings:
            if item["key"] == str(id_paciente).strip():
                stored_embedding = item["embedding"]

                # Convertir los embeddings en matrices 2D de forma (1, 1024)
                user_embedding_flat = np.array(user_embedding).reshape(-1)
                stored_embedding_flat = np.array(stored_embedding).reshape(-1)

                print(user_embedding_flat.shape)
                print(stored_embedding_flat.shape)

                print(user_embedding_flat.size)
                print(stored_embedding_flat.size)

                # Calcular la similitud del coseno
                similarity = cosine_similarity(user_embedding_flat, stored_embedding_flat)[0][0]

                if similarity > best_score:
                    # El mejor match actual se convierte en el segundo mejor
                    second_best_score = best_score
                    second_best_match = best_match

                    best_score = similarity
                    best_match = item

                elif similarity > second_best_score:
                    second_best_score = similarity
                    second_best_match = item

        # Mostrar la respuesta más relevante
        if best_match:
            print("se ha encontrado un best match: " + best_match)
            embeddings["content"] += f"Pregunta más similar encontrada: {best_match['question']} "
            embeddings["content"] += f"Respuesta: {best_match['answer']} "
            embeddings["content"] +=f"Contexto: {best_match['context']} "
        if second_best_match:
            print("se ha encontrado un second best match: " + second_best_match)
            embeddings["content"] +=f"\nSegunda mejor coincidencia encontrada: {second_best_match['question']} "
            embeddings["content"] +=f"Respuesta: {second_best_match['answer']} "
            embeddings["content"] +=f"Contexto: {second_best_match['context']}"
        else:
            print("no se encontraron matches relevantes")
            embeddings["content"] +="No se encontraron coincidencias relevantes."
    else:
        print("no se encontraron embeddings")
        embeddings["content"] +="No se encontraron embeddings."
    return embeddings

@app.route("/set-context", methods=["POST"])
def set_context():
    """Recibe el ID del paciente y carga su contexto desde los CSV."""
    try:
        data = request.get_json()
        id_paciente = int(data.get("id_paciente"))  # Convertir a entero

        if not id_paciente:
            print(jsonify({"error": "ID de paciente vacío"}), 400) 

        # Si ya existe el contexto, no lo recarga
        if id_paciente in contextos_pacientes:
            contexto = contextos_pacientes[id_paciente]
            print(jsonify({"message": "Contexto cargado correctamente"}))
        else:
            # Buscar información del paciente
            paciente_info = info_pacientes_df[info_pacientes_df["ID"] == id_paciente]
            notas_paciente = notas_df[notas_df["ID"] == id_paciente].head(2)  # Solo las dos primeras notas

            
            print(info_pacientes_df.head())  # Verifica que la columna y los datos están bien cargados
            print(info_pacientes_df.columns)

            if paciente_info.empty:
                return jsonify({"error": "Paciente no encontrado"}), 404

            # Convertir datos a string para pasarlo como contexto
            info_texto = paciente_info.to_string(index=False)
            notas_texto = notas_paciente.to_string(index=False) if not notas_paciente.empty else "Sin notas registradas."

            # Generar contexto
            contexto = f"""
            Eres una IA que asiste a personal sanitario para responder preguntas, generar informes, gráficas y orientar sobre un paciente concreto. 
            Como contexto inicial, te proporcionaré los siguientes datos del paciente:
            {info_texto}
    
            Y algunas notas tomadas:
            {notas_texto}
            
            Cuando se te haga una pregunta concreta, responderás con los datos proporcionados a eso y SOLO a eso, lo mismo con las gráficas, recuperarás
            solo los datos necesarios, cuando se te pida un resumen, resumirás en base a todos los datos que tengas y cuando se te pida consejo
            sobre pasos a seguir o recomendaciones para el paciente, recuperarás información relevante según el ámbito sobre el que se te pregunte.
            """

            # Guardar contexto en memoria
            contextos_pacientes[id_paciente] = contexto
            return jsonify({"message": "Contexto cargado correctamente"})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "El servidor Flask está funcionando correctamente"})

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        id_paciente = int(data.get("id_paciente"))

        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400
        
        messages = []
        
        messages.append({"role": "system", "content": contextos_pacientes[id_paciente]})

        messages.append(generarEmbedding(user_message, id_paciente))

        if id_paciente not in conversation_history:
            conversation_history[id_paciente] = []
            conversation_history[id_paciente].append({"role": "system", "content": "Este es el historial previo de la conversación:"})
        else:
            messages.extend(conversation_history[id_paciente])
        
        messages.append({"role": "user", "content": user_message})

        # Llamada a Amazon Bedrock usando litellm
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=messages
        )

        # Extraer la respuesta del modelo
        ai_response = response.choices[0].message.content
        print(ai_response)
    
        # Agrega el mensaje del usuario y la IA al historial
        conversation_history[id_paciente].append({"role": "user", "content": user_message})
        conversation_history[id_paciente].append({"role": "assistant", "content": ai_response})

        ai_response = "<p>"+ai_response+"</p>"
        
        # Devolver respuesta
        return jsonify({"response": ai_response})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)