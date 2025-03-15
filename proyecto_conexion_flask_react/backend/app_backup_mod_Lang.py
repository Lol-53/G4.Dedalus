from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
from langchain_anthropic import ChatAnthropic
import GraficaDatos as gd  # Importar las funciones de gráficos
import openai  # Utilizar el proxy de litellm para Amazon Bedrock

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",  # No compartir clave en mensajes públicos
    base_url="https://litellm.dccp.pbu.dedalus.com"  # No compartir URL en mensajes públicos
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Habilitar CORS para todas las rutas

# Configuración de LangChain con Claude-Sonnet en Bedrock
chat_model = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", "sk-lqIaTaCA6djhkYLWFx5Gww")  # Usa la variable de entorno o una clave fija
)

# Cargar datos de pacientes
info_pacientes_df = pd.read_csv("datos_pacientes/info_pacientes.csv")
notas_df = pd.read_csv("datos_pacientes/notas.csv")

# Almacenar contexto de pacientes en memoria
contextos_pacientes = {}
conversation_history = {}

@app.route("/set-context", methods=["POST"])
def set_context():
    """Carga el contexto del paciente y lo almacena en memoria."""
    try:
        data = request.get_json()
        id_paciente = int(data.get("id_paciente"))

        if id_paciente in contextos_pacientes:
            return jsonify({"message": "Contexto ya cargado"})

        paciente_info = info_pacientes_df[info_pacientes_df["PacienteID"] == id_paciente]
        notas_paciente = notas_df[notas_df["PacienteID"] == id_paciente].head(2)

        if paciente_info.empty:
            return jsonify({"error": "Paciente no encontrado"}), 404

        info_texto = paciente_info.to_string(index=False)
        notas_texto = notas_paciente.to_string(index=False) if not notas_paciente.empty else "Sin notas registradas."

        contexto = f"""
        Eres una IA que asiste a médicos con información sobre pacientes.
        Datos del paciente:
        {info_texto}
        
        Notas médicas:
        {notas_texto}
        """

        contextos_pacientes[id_paciente] = contexto
        return jsonify({"message": "Contexto cargado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    """Procesa preguntas sobre el paciente usando Claude-Sonnet en Amazon Bedrock o genera gráficos si es necesario."""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        id_paciente = int(data.get("id_paciente"))

        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400

        # Identificar si es una pregunta de gráfica
        if any(word in user_message.lower() for word in ["gráfico", "gráfica", "grafica", "dispersión", "histograma", "barras", "boxplot", "violín", "correlación", "tendencia"]):
            paciente_data = info_pacientes_df[info_pacientes_df["PacienteID"] == id_paciente]
            if paciente_data.empty:
                return jsonify({"error": "Paciente no encontrado"}), 404

            df = paciente_data.drop(columns=["PacienteID"])
            graph_type = "scatter" if "dispersión" in user_message else "histogram" if "histograma" in user_message else "bar" if "barras" in user_message else "boxplot" if "boxplot" in user_message else "violin" if "violín" in user_message else "trend" if "tendencia" in user_message else "correlation"
            x = "edad" if "edad" in user_message else "glucosa" if "glucosa" in user_message else "presion_sanguinea" if "presión" in user_message else None
            y = "glucosa" if "glucosa" in user_message else "presion_sanguinea" if "presión" in user_message else None

            graph_path = f"static/{graph_type}_{id_paciente}.png"

            if graph_type == "correlation":
                gd.graficaCorrelacion(df)
            elif graph_type == "scatter" and x and y:
                gd.graficaDispersion(df, x, y)
            elif graph_type == "histogram" and y:
                gd.graficaHistograma(df, y)
            elif graph_type == "bar" and x and y:
                gd.graficaBarras(df, x, y)
            elif graph_type == "boxplot" and x:
                gd.graficaBoxplot(df, x)
            elif graph_type == "violin" and x:
                gd.graficaViolin(df, x)
            elif graph_type == "trend" and x and y:
                gd.graficaCurvaTendencia(df, x, y)
            else:
                return jsonify({"error": "No se pudo detectar el tipo de gráfico."}), 400

            return jsonify({"response": graph_path})

        # Preguntas generales -> Enviar a Claude-Sonnet
        messages = [
            {"role": "system", "content": contextos_pacientes.get(id_paciente, "")},
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=messages
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
