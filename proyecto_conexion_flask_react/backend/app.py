from flask import Flask, request, jsonify
import openai  # Utiliza el proxy de litellm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas de Flask

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",
    base_url="https://litellm.dccp.pbu.dedalus.com"
)

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

        # Llamada a Amazon Bedrock usando litellm
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": user_message}]
        )

        # Extraer la respuesta del modelo
        ai_response = response.choices[0].message.content
        print(ai_response)
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)