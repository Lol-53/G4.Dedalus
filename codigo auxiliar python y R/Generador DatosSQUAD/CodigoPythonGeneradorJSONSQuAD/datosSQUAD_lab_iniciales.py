import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"C:\Users\mpord\Documents\3IngSoft\2Cuatri\G4.Dedalus\material_dedalus\DatosSQUAD\resumen_lab_iniciales.csv",encoding="utf-8")

# Convertir a formato SQuAD
data = {"data": []}

i = 0

for _, row in df.iterrows():
    i+=1
    titulo = f"{row['Fecha']} {row['Hora']}"
    context = (
        f"Paciente {row['PacienteID']} nombre Juan Pérez el día {row['Fecha']} y hora {row['Hora']}. "
        f"Glucosa: {row['Glucosa']} mg/dL. "

        f"Frecuencia Cardíaca: {row['FrecuenciaCardiaca']} latidos por minuto. "
        f"Temperatura: {row['Temperatura']}°C. "
        f"Frecuencia Respiratoria: {row['FrecuenciaRespiratoria']} respiraciones por minuto. "
        f"Saturación de Oxígeno: {row['SaturacionOxigeno']}%. "
        f"Leucocitos: {row['Leucocitos']} células/mm³. "
        f"Hemoglobina: {row['Hemoglobina']} g/dL. "
        f"Plaquetas: {row['Plaquetas']} células/mm³. "
        f"Colesterol: {row['Colesterol']} mg/dL. "
        f"HDL: {row['HDL']} mg/dL. "

    )

    preguntas = [
        {"question": "¿Cuál es la presión sistólica del paciente?", "id": i, "answers": [{"text": row['PresionSistolica'], "answer_start": context.find(str(row['PresionSistolica']))}]},
        {"question": "¿Cuál es la presión diastólica del paciente?", "id": i+1, "answers": [{"text": row['PresionDiastolica'], "answer_start": context.find(str(row['PresionDiastolica']))}]}, 
        {"question": "¿Cuál es la frecuencia cardiaca del paciente?", "id": i+2, "answers": [{"text": row['FrecuenciaCardiaca'], "answer_start": context.find(str(row['FrecuenciaCardiaca']))}]},
        {"question": "¿Cuál es la temperatura del paciente?", "id": i+3, "answers": [{"text": f"{row['Temperatura']}°C", "answer_start": context.find(str(row['Temperatura']))}]},
        {"question": "¿Cuál es la frecuencia respiratoria del paciente?", "id": i+4, "answers": [{"text": row['FrecuenciaRespiratoria'], "answer_start": context.find(str(row['FrecuenciaRespiratoria']))}]},
        {"question": "¿Cuál es la saturación de oxígeno del paciente?", "id":i+6, "answers": [{"text": f"{row['SaturacionOxigeno']}%", "answer_start": context.find(str(row['SaturacionOxigeno']))}]},
        {"question": "¿Cuál es el nivel de glucosa del paciente?", "id": i+7, "answers": [{"text": row['Glucosa'], "answer_start": context.find(str(row['Glucosa']))}]},
        {"question": "¿Cuántos leucocitos tiene el paciente?", "id": i+8, "answers": [{"text": row['Leucocitos'], "answer_start": context.find(str(row['Leucocitos']))}]},
        {"question": "¿Cuál es el nivel de hemoglobina del paciente?", "id": i+9, "answers": [{"text": row['Hemoglobina'], "answer_start": context.find(str(row['Hemoglobina']))}]},
        {"question": "¿Cuántas plaquetas tiene el paciente?", "id": i+10, "answers": [{"text": row['Plaquetas'], "answer_start": context.find(str(row['Plaquetas']))}]},
        {"question": "¿Cuál es el colesterol del paciente?", "id": i+11, "answers": [{"text": row['Colesterol'], "answer_start": context.find(str(row['Colesterol']))}]},
        {"question": "¿Cuál es el nivel de HDL del paciente?", "id": i+12, "answers": [{"text": row['HDL'], "answer_start": context.find(str(row['HDL']))}]},
        {"question": "¿Cuál es el nivel de LDL del paciente?", "id": i+13, "answers": [{"text": row['LDL'], "answer_start": context.find(str(row['LDL']))}]},
        {"question": "¿Cuál es el nivel de triglicéridos del paciente?", "id": i+14, "answers": [{"text": row['Trigliceridos'], "answer_start": context.find(str(row['Trigliceridos']))}]},
        {"question": "¿Cuál es el nivel de sodio del paciente?", "id": i+15, "answers": [{"text": row['Sodio'], "answer_start": context.find(str(row['Sodio']))}]},
        {"question": "¿Cuál es el nivel de potasio del paciente?", "id": i+16, "answers": [{"text": row['Potasio'], "answer_start": context.find(str(row['Potasio']))}]},
        {"question": "¿Cuál es el nivel de cloro del paciente?", "id": i+17, "answers": [{"text": row['Cloro'], "answer_start": context.find(str(row['Cloro']))}]},
        {"question": "¿Cuál es el nivel de creatinina del paciente?", "id": i+18, "answers": [{"text": row['Creatinina'], "answer_start": context.find(str(row['Creatinina']))}]},
        {"question": "¿Cuál es el nivel de urea del paciente?", "id": i+19, "answers": [{"text": row['Urea'], "answer_start": context.find(str(row['Urea']))}]},
        {"question": "¿Cuál es el nivel de AST del paciente?", "id": i+20, "answers": [{"text": row['AST'], "answer_start": context.find(str(row['AST']))}]},
        {"question": "¿Cuál es el nivel de ALT del paciente?", "id": i+21, "answers": [{"text": row['ALT'], "answer_start": context.find(str(row['ALT']))}]},
        {"question": "¿Cuál es el nivel de bilirrubina del paciente?", "id": i+22, "answers": [{"text": row['Bilirrubina'], "answer_start": context.find(str(row['Bilirrubina']))}]},
        {"question": "¿Cuál es el pH del paciente?", "id":  i+23, "answers": [{"text": row['pH'], "answer_start": context.find(str(row['pH']))}]},
        {"question": "¿Cuál es el pCO2 del paciente?", "id":  i+24, "answers": [{"text": row['pCO2'], "answer_start": context.find(str(row['pCO2']))}]},
        {"question": "¿Cuál es el pO2 del paciente?", "id":  i+25, "answers": [{"text": row['pO2'], "answer_start": context.find(str(row['pO2']))}]},
        {"question": "¿Cuál es el nivel de HCO3 del paciente?", "id":  i+26, "answers": [{"text": row['HCO3'], "answer_start": context.find(str(row['HCO3']))}]},
        {"question": "¿Cuál es el nivel de lactato del paciente?", "id":  i+27, "answers": [{"text": row['Lactato'], "answer_start": context.find(str(row['Lactato']))}]}
    ]

    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})
    i+=27

# Guardar en JSON
with open("dataset_squad_pacienteID1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")
