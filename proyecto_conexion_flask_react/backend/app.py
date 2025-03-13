from flask import Flask, request, jsonify
import openai  # Utiliza el proxy de litellm
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas de Flask

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

@app.route("/set-context", methods=["POST"])
def set_context():
    """Recibe el ID del paciente y carga su contexto desde los CSV."""
    try:
        data = request.get_json()
        id_paciente = data.get("id_paciente")

        if not id_paciente:
            return jsonify({"error": "ID de paciente vacío"}), 400

        # Si ya existe el contexto, no lo recarga
        if id_paciente in contextos_pacientes:
            contexto = contextos_pacientes[id_paciente]
        else:
            # Buscar información del paciente
            paciente_info = info_pacientes_df[info_pacientes_df["id"] == id_paciente]
            notas_paciente = notas_df[notas_df["id"] == id_paciente]

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

        # Llamada a Amazon Bedrock usando litellm
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": contexto}]
        )

        # Extraer la respuesta del modelo
        ai_response = response.choices[0].message.content
        print(ai_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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