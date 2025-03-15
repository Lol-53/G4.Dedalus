from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os
import re
import unicodedata
from flask_cors import CORS
from langchain_anthropic import ChatAnthropic
import GraficaDatos as gd  # Importar la función generarGrafica
import openai  # Utilizar el proxy de litellm para Amazon Bedrock

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",  # No compartir clave en mensajes públicos
    base_url="https://litellm.dccp.pbu.dedalus.com"  # No compartir URL en mensajes públicos
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Habilitar CORS para todas las rutas

# Asegurar que Flask sirva archivos de imágenes
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.getcwd(), filename)  # Sirve imágenes desde el directorio de trabajo

# Configuración de LangChain con Claude-Sonnet en Bedrock
chat_model = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", "sk-lqIaTaCA6djhkYLWFx5Gww")  # Usa la variable de entorno o una clave fija
)

# Cargar datos de pacientes y laboratorio
info_pacientes_df = pd.read_csv("datos_pacientes/info_pacientes.csv")
notas_df = pd.read_csv("datos_pacientes/notas.csv")
lab_df = pd.read_csv("datos_pacientes/resumen_lab_iniciales.csv")  # Nuevo archivo de laboratorio

# Convertir nombres de columnas a minúsculas para evitar errores
lab_df.columns = lab_df.columns.str.lower()

# Almacenar contexto de pacientes en memoria
contextos_pacientes = {}
conversation_history = {}

@app.route("/set-context", methods=["POST"])
def set_context():
    """Carga el contexto del paciente y lo almacena en memoria."""
    try:
        data = request.get_json()
        id_paciente = str(data.get("id_paciente"))

        if id_paciente in contextos_pacientes:
            return jsonify({"message": "Contexto ya cargado"})

        paciente_info = info_pacientes_df[info_pacientes_df["PacienteID"] == int(id_paciente)]
        notas_paciente = notas_df[notas_df["PacienteID"] == int(id_paciente)].head(2)

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
        id_paciente = str(data.get("id_paciente"))

        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400

        # Recuperar contexto del paciente
        contexto_paciente = contextos_pacientes.get(id_paciente, "")
        if not contexto_paciente:
            return jsonify({"error": "No se ha establecido el contexto para este paciente."}), 400

        messages = [
            {"role": "system", "content": contexto_paciente},
            {"role": "user", "content": user_message}
        ]

        # Verificar si la pregunta es sobre gráficos
        graficos_disponibles = {
            "correlacion": "graficaCorrelacion",
            "correlación": "graficaCorrelacion",
            "dispersión": "graficaDispersion",
            "dispersion": "graficaDispersion",
            "histograma": "graficaHistograma",
            "istograma": "graficaHistograma",
            "barras": "graficaBarras",
            "boxplot": "graficaBoxplot",
            "violín": "graficaViolin",
            "violin": "graficaViolin",
            "tendencia": "graficaCurvaTendencia"
        }

        graficos_seleccionados = [nombre for palabra, nombre in graficos_disponibles.items() if palabra in user_message.lower()]

        if graficos_seleccionados:
            palabras_usuario = re.sub(r'[^\w\s]', '', user_message.lower()).split()
            variables_encontradas = [col for col in lab_df.columns if any(palabra.lower() in col.lower() for palabra in palabras_usuario)]

            x = variables_encontradas[0] if len(variables_encontradas) > 0 else None
            y = variables_encontradas[1] if len(variables_encontradas) > 1 else None

            if not x:
                return jsonify({"error": "No se encontró una variable válida en los datos."}), 400

            print(f"Llamando a generarGrafica con: id_paciente={id_paciente}, x={x}, y={y}, tipo={graficos_seleccionados}")
            # Llamar a la función generarGrafica
            paths_imagenes = gd.generarGrafica("lab_iniciales", id_paciente, x, y, graficos_seleccionados)
            #imagenes_urls = [f"/images/{os.path.basename(path)}" for path in paths_imagenes if path]
            ai_response2 = "<p>"+"<img src="+ '"' + paths_imagenes[0]+ '"' + ">" +"</p>"
            return jsonify({"response": ai_response2})

        # Si no es una pregunta sobre gráficos, usar Claude-Sonnet
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
