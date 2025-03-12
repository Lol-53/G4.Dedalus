from flask import Flask, request, jsonify
import openai  # Utiliza el proxy de litellm
import faiss  # Se añade FAISS para búsqueda vectorial
import numpy as np  # Se añade NumPy para manejar embeddings
from flask_cors import CORS
import litellm  # Importa litellm

litellm.drop_params = True

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas de Flask

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
    base_url="https://litellm.dccp.pbu.dedalus.com"
)

documentos = [
    "Paciente Juan Pérez, diabetes tipo 2, tratamiento con insulina.",
    "Paciente María López, hipertensión, dieta baja en sal y ejercicio.",
    "Paciente Pedro Gómez, colesterol alto, estatinas y control de peso."
]

response = client.models.list()
print(response)

def obtener_embedding(texto):
    response = client.embeddings.create(
        model="bedrock/amazon.titan-embed-text-v2:0",
        input=texto
    )
    return response.data[0].embedding  # Extrae el embedding generado


vectores = np.array([obtener_embedding(doc) for doc in documentos])
dim = vectores.shape[1]  # Dimensión del embedding
index = faiss.IndexFlatL2(dim)
index.add(vectores)
texto_por_indice = {i: documentos[i] for i in range(len(documentos))}

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "El servidor Flask está funcionando correctamente"})

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400

        vector_pregunta = obtener_embedding(user_message).reshape(1, -1)

        k = 2  # Número de resultados a recuperar
        _, indices = index.search(vector_pregunta, k)
        contexto = "\n".join([texto_por_indice[idx] for idx in indices[0]])

        # Llamada a Amazon Bedrock usando litellm
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[
                {"role": "system", "content": "Usa el siguiente contexto para responder preguntas:"},
                {"role": "system", "content": contexto},
                {"role": "user", "content": user_message}
            ]
        )

        # Extraer la respuesta del modelo
        ai_response = response.choices[0].message.content
        print(ai_response)
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)