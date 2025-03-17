import json
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os
import re
import requests
import unicodedata
from flask_cors import CORS
from langchain_anthropic import ChatAnthropic
import GraficaDatos as gd  # Importar la función generarGrafica
import openai  # Utilizar el proxy de litellm para Amazon Bedrock
from sklearn.metrics.pairwise import cosine_similarity
import csv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Habilitar CORS para todas las rutas

# Configurar la conexión con Bedrock usando litellm
client = openai.OpenAI(
    api_key="sk-lqIaTaCA6djhkYLWFx5Gww",  # No compartir clave en mensajes públicos
    base_url="https://litellm.dccp.pbu.dedalus.com"  # No compartir URL en mensajes públicos
)

DATA_PATH = "historiales/"

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

# Asegurar que exista la carpeta de historiales
os.makedirs(DATA_PATH, exist_ok=True)

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

    if user_embedding:
        best_match = None
        best_score = -1
        second_best_match = None
        second_best_score = -1

        for item in all_embeddings:
            if item["key"] == str(id_paciente).strip():
                stored_embedding = item["embedding"]

                # Convert embeddings to numpy arrays
                user_embedding_array = np.array(user_embedding)
                stored_embedding_array = np.array(stored_embedding)

                # Ensure they are 2D arrays for cosine_similarity
                if user_embedding_array.ndim == 1:
                    user_embedding_array = user_embedding_array.reshape(1, -1)
                if stored_embedding_array.ndim == 1:
                    stored_embedding_array = stored_embedding_array.reshape(1, -1)

                # Calculate cosine similarity
                similarity = cosine_similarity(user_embedding_array, stored_embedding_array)[0][0]

                # Update best matches
                if similarity > best_score:
                    # Current best becomes second best
                    second_best_score = best_score
                    second_best_match = best_match

                    best_score = similarity
                    best_match = item

                elif similarity > second_best_score:
                    second_best_score = similarity
                    second_best_match = item

        # Return the most relevant responses
        if best_match:
            print("se ha encontrado un best match: " + str(best_match))
            embeddings["content"] += f"Pregunta más similar encontrada: {best_match['question']} "
            embeddings["content"] += f"Respuesta: {best_match['answer']} "
            embeddings["content"] += f"Contexto: {best_match['context']} "
        if second_best_match:
            print("se ha encontrado un second best match: " + str(second_best_match))
            embeddings["content"] += f"\nSegunda mejor coincidencia encontrada: {second_best_match['question']} "
            embeddings["content"] += f"Respuesta: {second_best_match['answer']} "
            embeddings["content"] += f"Contexto: {second_best_match['context']}"
        else:
            print("no se encontraron matches relevantes")
            embeddings["content"] += "No se encontraron coincidencias relevantes."
    else:
        print("no se encontraron embeddings")
        embeddings["content"] += "No se encontraron embeddings."
    print(embeddings)
    return embeddings

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

@app.route("/add-patient", methods=["POST"])
def get_paciente():
    try:
        # Obtener los datos del paciente desde el cuerpo de la solicitud (JSON)
        data = request.get_json()

        # Extraer la información del paciente
        id_paciente = data.get("id_paciente")
        nombre = data.get("nombre")
        edad = data.get("edad")
        sexo = data.get("sexo")
        alergias = data.get("alergias")
        motivo_ingreso = data.get("motivoIngreso")
        diagnostico_principal = data.get("diagnosticoPrincipal")
        condiciones_previas = data.get("condicionesPrevias")
        fecha_ingreso = data.get("fechaIngreso")
        servicio = data.get("servicio")
        estado_al_ingreso = data.get("estadoAlIngreso")
        cama = data.get("cama")
        nuhsa = data.get("nuhsa")

        # Abre el archivo CSV en modo de adición
        with open('patients.csv', mode='a', newline='') as infopacientes:
            writer = csv.writer(infopacientes)

            # Escribir los datos del paciente como una nueva fila en el archivo CSV
            writer.writerow([id_paciente, nombre, edad, sexo, alergias, motivo_ingreso, diagnostico_principal,
                             condiciones_previas, fecha_ingreso, servicio, estado_al_ingreso, cama, nuhsa])

        return jsonify({"message": "Paciente agregado correctamente"}), 200
    except Exception as e:
        return jsonify({"message": "Error al agregar paciente", "error": str(e)}), 500

@app.route("/get-history", methods=["POST"])
def get_history():
    try:
        data = request.get_json()
        id_paciente = str(data.get("id_paciente"))
        with open(f"{DATA_PATH}{id_paciente}.json", "r") as f:
            historial = json.load(f)
        return jsonify(historial)
    except FileNotFoundError:
        return jsonify({"error": "Historial no encontrado"}), 404


@app.route("/set-context", methods=["POST"])
def set_context():
    """Carga el contexto del paciente y lo almacena en memoria."""
    try:
        data = request.get_json()
        id_paciente = str(data.get("id_paciente"))

        if not id_paciente:
            print("ID de paciente vacío")
            print(jsonify({"error": "ID de paciente vacío"}), 400)

        # Si ya existe el contexto, no lo recarga
        if id_paciente in contextos_pacientes:
            contexto = contextos_pacientes[id_paciente]
            print(jsonify({"message": "Contexto cargado correctamente"}))
        else:
            # Buscar información del paciente
            id_paciente = int(id_paciente)

            paciente_info = info_pacientes_df[info_pacientes_df["ID"] == id_paciente]
            notas_paciente = notas_df[notas_df["ID"] == id_paciente].head(2)  # Solo las dos primeras notas

            if paciente_info.empty:
                print("error Paciente no encontrado")
                return jsonify({"error": "Paciente no encontrado"}), 404

            info_texto = paciente_info.to_string(index=False)
            notas_texto = notas_paciente.to_string(index=False) if not notas_paciente.empty else "Sin notas registradas."

            contexto = f"""
            Eres una IA que asiste a personal sanitario para responder preguntas, generar informes, gráficas y orientar sobre un paciente concreto.
            Como contexto inicial, te proporcionaré los siguientes datos del paciente:
            {info_texto}

            Y algunas notas tomadas:
            {notas_texto}

            Cuando se te haga una pregunta concreta, responderás con los datos proporcionados a eso y SOLO a eso, lo mismo con las gráficas, recuperarás
            solo los datos necesarios, cuando se te pida un resumen, resumirás en base a todos los datos que tengas y cuando se te pida consejo
            sobre pasos a seguir o recomendaciones para el paciente, recuperarás información relevante según el ámbito sobre el que se te pregunte.
            
            También se te proporcionan otros datos que el sistema encuentra en base a la pregunta del usuario y vienen con el siguiete prefijo:
            "información relevante ofrecida en formato json SQUaD:"
            Pon especial atención a esos datos para responder preguntas concretas sobre dosis del paciente, mediciones, anomalías, todo lo que
            se incluya en ese mensaje, es información relevante que debes tener en cuenta para responder.
            """

            contextos_pacientes[id_paciente] = contexto
            return jsonify({"message": "Contexto cargado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def loadHistory(paciente_id):
    try:
        with open(f"{DATA_PATH}{paciente_id}.json", "r") as f:
            history = json.load(f)
        return history
    except FileNotFoundError:
        return []


def saveHistory(history, paciente_id):
    with open(f"{DATA_PATH}{paciente_id}.json", "w") as f:
        json.dump(history, f, indent=2)
    pass


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    """Procesa preguntas sobre el paciente usando Claude-Sonnet en Amazon Bedrock o genera gráficos si es necesario."""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        id_paciente = str(data.get("id_paciente"))

        conversation_history = loadHistory(id_paciente)

        if not user_message:
            print("Mensaje vacío USUARIO")
            return jsonify({"error": "Mensaje vacío"}), 400

        conversation_history.append({"role": "user", "content": user_message, "type": "text"})

        # Recuperar contexto del paciente

        id_paciente = int(id_paciente)

        contexto_paciente = contextos_pacientes[id_paciente]

        if not contexto_paciente:
            print("No se ha establecido el contexto para este paciente.")
            return jsonify({"error": "No se ha establecido el contexto para este paciente."}), 400


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
                print("No se encontró una variable válida en los datos.")
                return jsonify({"error": "No se encontró una variable válida en los datos."}), 400

            print(f"Llamando a generarGrafica con: id_paciente={id_paciente}, x={x}, y={y}, tipo={graficos_seleccionados}")
            # Llamar a la función generarGrafica
            paths_imagenes = gd.generarGrafica("lab_iniciales", id_paciente, x, y, graficos_seleccionados)
            #imagenes_urls = [f"/images/{os.path.basename(path)}" for path in paths_imagenes if path]
            ai_response2 = f'{paths_imagenes[0]}'

            conversation_history.append({"role": "assistant", "content": ai_response2, "type": "image"})

            saveHistory(conversation_history, id_paciente)

            return conversation_history


        messages = [{"role": "system", "content": contextos_pacientes[id_paciente]},
                    generarEmbedding(user_message, id_paciente),
                    {"role": "system", "content": "Este es el historial previo de la conversación:"}]

        conversation_history_adapted = conversation_history.copy()

        for mensaje in conversation_history_adapted:
            mensaje.pop("text", None)

        messages.extend(conversation_history_adapted)

        messages.append({"role": "user", "content": user_message})

        # Si no es una pregunta sobre gráficos, usar Claude-Sonnet
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=messages
        )

        ai_response = response.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": ai_response, "type": "text"})

        print(conversation_history)

        saveHistory(conversation_history, id_paciente)

        return conversation_history
    except Exception as e:
        print(e.args)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
