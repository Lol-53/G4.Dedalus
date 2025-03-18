import json
import traceback

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
import GeneraPDF as gpdf  # Importar la función generarGrafica
import generardorJSONResumen as gjson  # Importar la función generarGrafica
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

def generarEmbedding(user_message, id_paciente, num_matches=3, similarity_threshold=0.7, current_matches=[], user_embedding=None):
    """
    Generates embeddings and finds the top N most similar matches that exceed a minimum similarity threshold.

    Args:
        user_message: The user's message to generate embeddings for
        id_paciente: The patient ID to filter embeddings
        num_matches: Number of best matches to return (default: 5)
        similarity_threshold: Minimum similarity score required (default: 0.8)

    Returns:
        A dictionary with relevant information in SQuAD format
    """

    embeddings = {"role": "system", "content": "información relevante ofrecida en formato json SQUaD: "}

    if (similarity_threshold <= 0.2):
        embeddings["content"] += "No se encontraron embeddings."
        return embeddings

    if len(current_matches)==num_matches:
        top_matches = current_matches

        for i, (match, score) in enumerate(top_matches):
            rank = i + 1
            print(f"se ha encontrado match #{rank}: {str(match)} con puntuación: {score:.4f}")

            if i == 0:
                prefix = "Pregunta más similar encontrada: "
            else:
                prefix = f"\nCoincidencia #{rank} encontrada: "

            embeddings["content"] += f"{prefix}{match['question']} "
            embeddings["content"] += f"Respuesta: {match['answer']} "
            embeddings["content"] += f"Contexto: {match['context']} "
            embeddings["content"] += f"(Similitud: {score:.4f}) "

        print(embeddings)
        return embeddings

    if not user_embedding:
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
        # Create a list to store all matches with their scores
        all_matches = []
        existing_items = [match_tuple[0] for match_tuple in current_matches]

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

                # Only add matches that exceed the similarity threshold
                if similarity >= similarity_threshold and item not in existing_items:
                    all_matches.append((item, similarity))

        # Sort matches by similarity score in descending order
        all_matches.sort(key=lambda x: x[1], reverse=True)

        # Take only the top N matches
        top_matches = all_matches[:num_matches]

        # If we found matches, add them to the response
        if top_matches:
            if len(current_matches) + len(top_matches) > num_matches  :
                excess = ( len(top_matches) + len(current_matches) ) - num_matches
                top_matches = top_matches[:num_matches-excess]

            return generarEmbedding(
                user_message,
                id_paciente,
                num_matches=num_matches,
                similarity_threshold=similarity_threshold-0.0015,
                current_matches=current_matches + top_matches,
                user_embedding=user_embedding
            )
        else:
            print("no se encontraron matches relevantes que superen el umbral de similitud " + str(similarity_threshold))
            return generarEmbedding(
                user_message,
                id_paciente,
                num_matches=num_matches,
                similarity_threshold=similarity_threshold-0.0015,
                user_embedding=user_embedding)

    print("no se pudo hacer embedding de la pregunta del usuario")
    embeddings["content"] += "No se encontraron embeddings."
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

@app.route("/csv", methods=["GET"])
def get_csv():
    # Obtener la ruta absoluta correcta
    base_dir = os.getcwd()  # Obtiene el directorio donde se ejecuta el script
    csv_dir = os.path.join(base_dir, "datos_pacientes")  # Ruta absoluta al directorio
    csv_path = os.path.join(csv_dir, "info_pacientes.csv")  # Ruta completa al archivo

    # Verificar si el archivo existe
    if not os.path.exists(csv_path):
        print("Error: no se ha encontrado el archivo CSV con los datos de los pacientes")
        return jsonify({"error": "No se ha encontrado el archivo CSV con los datos de los pacientes"}), 404

    # Enviar el archivo
    return send_from_directory(csv_dir, "info_pacientes.csv")

@app.route("/add-patient", methods=["POST"])
def get_paciente():
    try:
        # Obtener los datos del paciente desde el cuerpo de la solicitud (JSON)
        data = request.get_json()
        print("Datos recibidos:", data)

        # Extraer la información del paciente
        id_paciente = data.get("id_paciente")
        nombre = data.get("nombre")
        edad = data.get("edad")  # No entre comillas
        sexo = data.get("sexo")
        alergias = data.get("alergias")
        motivo_ingreso = data.get("motivoIngreso")
        diagnostico_principal = data.get("diagnosticoPrincipal")
        condiciones_previas = data.get("condicionesPrevias")
        fecha_ingreso =data.get("fechaIngreso")
        servicio = data.get("servicio")
        estado_al_ingreso = data.get("estadoAlIngreso")
        cama = data.get("cama")  # No entre comillas
        nuhsa = data.get("nuhsa")

        # Ruta absoluta del archivo CSV
        csv_path = os.path.join(os.getcwd(), "datos_pacientes", "info_pacientes.csv")
        print("Ruta del CSV:", csv_path)  # 👈 Imprime la ruta completa del archivo

        # Abre el archivo CSV en modo de adición
        with open(csv_path, mode='a', newline='', encoding='utf-8') as infopacientes:
            writer = csv.writer(infopacientes)
            writer.writerow([id_paciente, nombre, edad, sexo, alergias, motivo_ingreso, diagnostico_principal,
                             condiciones_previas, fecha_ingreso, servicio, estado_al_ingreso, cama, nuhsa])

        print("Paciente agregado correctamente")  # 👈 Confirma que la escritura fue exitosa
        return jsonify({"message": "Paciente agregado correctamente"}), 200

    except Exception as e:
        return jsonify({"message": "Error al agregar paciente", "error": str(e)}), 500

@app.route("/get-history", methods=["POST"])
def get_history():
    try:
        data = request.get_json()
        id_paciente = str(data.get("id_paciente"))
        print("coge el id: "+id_paciente)
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
            Eres una IA que asiste a personal sanitario para responder preguntas, resumir información, y dar pasos a seguir u orientar 
            sobre un paciente concreto. Como contexto inicial, te proporcionaré los siguientes datos del paciente:
            {info_texto}

            Y algunas notas tomadas:
            {notas_texto}

            Cuando se te haga una pregunta concreta, responderás con los datos proporcionados a eso y SOLO a eso, cuando se te pida un resumen, resumirás en base a todos los datos que tengas 
            y cuando se te pida consejo sobre pasos a seguir o recomendaciones para el paciente, recuperarás información relevante según el ámbito sobre el que se te pregunte y también podrás
            en ese caso aportar otra información externa a los datos proporcionado que ayude a orientar al usuario.
            
            También se te proporcionan otros datos que el sistema encuentra en base a la pregunta del usuario y vienen con el siguiete prefijo:
            "información relevante ofrecida en formato json SQUaD:"
            Pon especial atención a esos datos para responder preguntas concretas sobre dosis del paciente, mediciones, anomalías, así como para dar los pasos a seguir o recomendaciones.
            Todo lo que se incluya en ese mensaje  es información relevante que debes tener en cuenta para responder.
            
            También es importante ofrecer la información de manera visual, cuando des una lista de valores (1., 2. ... ó a), b) ...), introduce saltos de línea, tauladores,
            cualquier cosa que permita ver de manera visual la información, no te limites a copiar y pegar la información que se te ofrece en ese aspecto, y si se te pide
            un resumen, también sería interesante dividirlo en apartados y dejar más bonita la información.
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


def esDeGraficos(user_message, id_paciente, conversation_history):
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
            return False

        print(f"Llamando a generarGrafica con: id_paciente={id_paciente}, x={x}, y={y}, tipo={graficos_seleccionados}")
        # Llamar a la función generarGrafica
        paths_imagenes = gd.generarGrafica("lab_iniciales", str(id_paciente), x, y, graficos_seleccionados)
        #imagenes_urls = [f"/images/{os.path.basename(path)}" for path in paths_imagenes if path]
        ai_response2 = f'{paths_imagenes[0]}'

        conversation_history.append({"role": "assistant", "content": ai_response2, "type": "image"})

        saveHistory(conversation_history, id_paciente)

        return conversation_history


def obtener_diagnostico(path_CSV_pacientes:str,ID:str):

    diagnostico= "No se encontro diagnóstico"
    df = pd.read_csv(path_CSV_pacientes)
    print(df.columns)

    datos_id = df[df["ID"]==ID]

    print(datos_id)

    return datos_id.iloc[0]["DiagnosticoPrincipal"]


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
        graficos = esDeGraficos(user_message, id_paciente, conversation_history)
        if graficos:
            return graficos


        messages = [{"role": "system", "content": contextos_pacientes[id_paciente]}]

        # DETECTAR RECOMENDACION:

        frases_recomendacion = [
            "pasos a seguir", "recomendaciones", "siguientes pasos",
            "siguientes acciones", "recomiéndame", "recomiendame",
            "qué debo hacer", "que debo hacer"
        ]

        detectar_recomendacion = any(frase in user_message.lower() for frase in frases_recomendacion)

        if detectar_recomendacion:
            messages.append({"role": "system", "content": f"""Asume el rol de un médico o asistente médico experto . Un paciente ha sido diagnosticado con {obtener_diagnostico("datos_pacientes/info_pacientes.csv", id_paciente)} 
                y necesita una guía detallada sobre las acciones que debe tomar. Proporciona información clara y práctica sobre los siguientes aspectos:_   
                3. **Tratamiento recomendado:** Indica los tratamientos médicos habituales (medicamentos, terapias, cambios en el estilo de vida).  
                4. **Cuidados diarios y recomendaciones:** Consejos sobre alimentación, ejercicio, descanso y otros hábitos saludables.  
                5. **Cuándo buscar ayuda médica:** Señales de alerta que requieren atención médica urgente.  
                6. **Pronóstico y evolución:** Qué esperar a corto y largo plazo si se siguen las indicaciones adecuadas.  
                
                _Asegúrate de proporcionar información precisa, basada en evidencia médica actual. Responde de manera clara, estructurada y con un tono empático._"""})
            messages.append(generarEmbedding(user_message, id_paciente, 10, 0.65))
        else:
            messages.append(generarEmbedding(user_message, id_paciente))

        messages.append({"role": "system", "content": "Este es el historial previo de la conversación:"})

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
        print("error en ask-ai:")
        print(e.args)
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/generate-report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()

        messages = [{"role": "system", "content":"""
            Genera el contenido un pdf con el resumen clínico detallado basado en la evolución del paciente, de los datos de laboratorio iniciales, de la medicación, de las notas, procedimientos e información médica relacionada con el paciente.
            
            El resumen tiene que tener como título "Resumen Clínico de " con el nombre del paciente. Luego un subtítulo con la fecha del ingreso del paciente. El resto de secciones debe de seguir el formato de Heading1.
            
            El resumen debe incluir las siguientes secciones: Datos del paciente, Motivo de Ingreso, Antecedentes médicos, Estado clínico actual, Pruebas realizadas, notas medicas realizadas con sus respectivas fechas ,Tratamiento y recomendaciones.
            
            Si en alguna sección no existen datos o se queda vacía, se deberá de poner "No se tiene información de {Nombre Sección vacía}" donde nombre sección vacía corresponde con el nombre de la sección que no tiene ningún dato.
            
            Información médica del paciente:
            
            Primera sección de Datos del paciente:
            Nombre del paciente: [Nombre completo del paciente]
            Edad: [Edad del paciente] años
            Sexo: [Masculino/Femenino]
            Identificador: [Número ID del paciente]
            Cama: [número de cama que ocupa el paciente]
            NUHSA: [Código NUHSA asociado al paciente]
            Diagnostico Principal: [Codigo del Diagnóstico Principal]
            
            Segunda sección Motivo del Ingreso:
            Motivo de ingreso: [Descripción del estado del ingreso por el cual el paciente está buscando atención médica o ha recibido atención médica]
            
            
            Tercera sección Antecedentes médicos:
            Antecedentes médicos: [Descripción de enfermedades o condiciones previas del paciente, como enfermedades crónicas, cirugías previas, etc.]
            Alérgias: [Descripción de las alérgias que presenta el paciente]
            
            
            Cuarta sección Estado clínico actual:
            Síntomas al ingreso: [Descripción de los síntomas actuales del paciente al momento de la consulta o ingreso]
            Evolución del paciente: [Descripción de la evolución de los síntomas del paciente junto a la flecha del estudio de la evolución]
            Diagnóstico inicial: [Descripción del diagnóstico inicial]
            
            
            Quinta sección Pruebas realizadas:
            Resultados de Laboratorio: [Listado de valores y magnitudes de pruebas realizadas en el laboratorio del paciente]
            Pruebas realizadas: [Descripción de las pruebas o procedimientos que se han realizado al paciente, como  radiografías, ecografías, etc.]
            
            Sexta sección Notas médicas:
            Notas médicas: [Registros, en formato lista "fecha,nota realizada", del paciente realizados por personal médico junto con su fecha de realización]
            
            
            
            Séptima sección Tratamiento y Recomendaciones:
            Tratamiento administrado: [Descripción de los tratamientos que se le han administrado al paciente, como medicamentos con la dosis y vía, intervenciones quirúrgicas, terapias, etc.]
            Estado clínico actual: [Descripción del estado clínico del paciente tras las intervenciones iniciales, incluyendo mejoría o complicaciones]
            
            
            Genera un resumen clínico con la siguiente estructura:
            Resumen Clínico del nombre paciente
            Fecha de ingreso
            
            Datos del paciente:
            
            Nombre completo
            Edad
            Sexo
            Identificador
            Cama
            Código NUHSA
            
            Motivo de Ingreso:
            
            Breve descripción del motivo que llevó al paciente a buscar atención médica.
            Antecedentes médicos:
            
            Enfermedades crónicas, cirugías previas, antecedentes familiares relevantes.
            Estado clínico actual:
            
            Descripción de los síntomas actuales, diagnóstico y evolución del estado del paciente.
            Pruebas realizadas:
            
            Listado y detalle de las pruebas realizadas, los resultados obtenidos con sus magnitudes y el diagnóstico a partir de las mismas.
            Notas médicas:
            
            Listado de las fechas y notas realizadas al paciente por el personal médico.
            Tratamiento y recomendaciones:
            
            Detalles del tratamiento administrado (medicamentos, terapias) y recomendaciones para el seguimiento.
            Notas adicionales:
            
            Aquí, en base a la información obtenida a lo largo de la conversación suministrada y todos los datos que hayas recibido, puedes
            hacer algún apunte como lo haría un Doctor, como una especie de conclusión con un enfoque más humano
            
            
            """}]
        csv_files = [
            "datos_pacientes/info_pacientes.csv",
            "datos_pacientes/notas.csv",
            "datos_pacientes/resumen_evolucion.csv",
            "datos_pacientes/resumen_evolucion_p1.csv",
            "datos_pacientes/resumen_evolucion_p2.csv",
            "datos_pacientes/resumen_evolucion_process.csv",
            "datos_pacientes/resumen_lab_iniciales.csv",
            "datos_pacientes/resumen_medicacion.csv",
            "datos_pacientes/resumen_procedimientos.csv"
        ]


        csv_data = gjson.csv_a_json_por_id(csv_files, data.get("id_paciente"))
        csv_data = json.dumps(csv_data, ensure_ascii=False, indent=2)

        messages.append({"role": "system", "content": csv_data})

        conversation_history = loadHistory(data.get("id_paciente"))

        conversation_history_adapted = conversation_history.copy()

        for mensaje in conversation_history_adapted:
            mensaje.pop("text", None)

        messages.extend(conversation_history_adapted)

        print(csv_data)

        messages.append({"role": "user", "content": "generame un resumen con los datos del paciente"})

        print("he pasado append 2")

        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=messages
        )
        print("he creado response")

        ai_response = response.choices[0].message.content
        print(ai_response)

        gpdf.GeneraPDF(ai_response)
        print("no tengo ni idea de que ocurre")
        return jsonify({"informe": ai_response})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
