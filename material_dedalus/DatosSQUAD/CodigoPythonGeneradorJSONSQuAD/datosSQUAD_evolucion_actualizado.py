import pandas as pd
import json

# Cargar el DataFrame desde CSV
df = pd.read_csv(r"CSV\resumen_evolucion_process.csv", encoding="utf-8")

# Construir la estructura del nuevo JSON en formato SQuAD
data = {"data": []}

i = 0

for _, row in df.iterrows():
    i+=1
    titulo = f"{row['Fecha']} {row['Hora']}"
    context = (
        f"Paciente {row['ID']} el día {row['Fecha']} y hora {row['Hora']}. "
        f"Presión Sistólica: {row['PresionSistolica']} mmHg. "
        f"Presión Diastólica: {row['PresionDiastolica']} mmHg. "
        f"Frecuencia Cardíaca: {row['FrecuenciaCardiaca']} latidos por minuto. "
        f"Temperatura: {row['Temperatura']}°C. "
        f"Frecuencia Respiratoria: {row['FrecuenciaRespiratoria']} respiraciones por minuto. "
        f"Saturación de Oxígeno: {row['SaturacionOxigeno']}%. "
        f"Glucosa: {row['Glucosa']} mg/dL. "
        f"Leucocitos: {row['Leucocitos']} células/mm³. "
        f"Hemoglobina: {row['Hemoglobina']} g/dL. "
        f"Plaquetas: {row['Plaquetas']} células/mm³. "
        f"Colesterol: {row['Colesterol']} mg/dL. "
        f"HDL: {row['HDL']} mg/dL. "
        f"LDL: {row['LDL']} mg/dL. "
        f"Triglicéridos: {row['Trigliceridos']} mg/dL. "
        f"Sodio: {row['Sodio']} mEq/L. "
        f"Potasio: {row['Potasio']} mEq/L. "
        f"Cloro: {row['Cloro']} mEq/L. "
        f"Creatinina: {row['Creatinina']} mg/dL. "
        f"Urea: {row['Urea']} mg/dL. "
        f"AST: {row['AST']} U/L. "
        f"ALT: {row['ALT']} U/L. "
        f"Bilirrubina: {row['Bilirrubina']} mg/dL. "
        f"pH: {row['pH']}. "
        f"pCO2: {row['pCO2']} mmHg. "
        f"pO2: {row['pO2']} mmHg. "
        f"HCO3: {row['HCO3']} mEq/L. "
        f"Lactato: {row['Lactato']} mmol/L. "
    )
    
    preguntas = [
        {"question": "¿Cuál es la presión sistólica del paciente?", "id": i, "answers": [{"text": row['PresionSistolica'], "answer_start": context.find(str(row['PresionSistolica']))}]},
        {"question": "¿Cuál es la presión diastólica del paciente?", "id": i+1, "answers": [{"text": presion_diastolica, "answer_start": context.find(str(presion_diastolica))}]},
        {"question": "¿Cuál es la frecuencia cardiaca del paciente?", "id": i+2, "answers": [{"text": frecuencia_cardiaca, "answer_start": context.find(str(frecuencia_cardiaca))}]},
        {"question": "¿Cuál es la temperatura del paciente?", "id":i+3, "answers": [{"text": f"{temperatura}°C", "answer_start": context.find(str(temperatura))}]},
        {"question": "¿Cuál es la frecuencia respiratoria del paciente?", "id":i+4, "answers": [{"text": frecuencia_respiratoria, "answer_start": context.find(str(frecuencia_respiratoria))}]},
        {"question": "¿Cuál es la saturación de oxígeno del paciente?", "id":i+5, "answers": [{"text": f"{saturacion_oxigeno}%", "answer_start": context.find(str(saturacion_oxigeno))}]},
        {"question": "¿Cuál es el nivel de glucosa del paciente?", "id":i+6, "answers": [{"text": glucosa, "answer_start": context.find(str(glucosa))}]},
        {"question": "¿Cuántos leucocitos tiene el paciente?", "id":i+7, "answers": [{"text": leucocitos, "answer_start": context.find(str(leucocitos))}]},
        {"question": "¿Cuál es el nivel de hemoglobina del paciente?", "id":i+8, "answers": [{"text": hemoglobina, "answer_start": context.find(str(hemoglobina))}]},
        {"question": "¿Cuántas plaquetas tiene el paciente?", "id": i+9, "answers": [{"text": plaquetas, "answer_start": context.find(str(plaquetas))}]},
        {"question": "¿Cuál es el colesterol del paciente?", "id": i+10, "answers": [{"text": colesterol, "answer_start": context.find(str(colesterol))}]},
        {"question": "¿Cuál es el nivel de HDL del paciente?", "id": i+11, "answers": [{"text": hdl, "answer_start": context.find(str(hdl))}]},
        {"question": "¿Cuál es el nivel de LDL del paciente?", "id": i+12, "answers": [{"text": ldl, "answer_start": context.find(str(ldl))}]},
        {"question": "¿Cuál es el nivel de triglicéridos del paciente?", "id": i+13, "answers": [{"text": trigliceridos, "answer_start": context.find(str(trigliceridos))}]},
        {"question": "¿Cuál es el nivel de sodio del paciente?", "id": i+14, "answers": [{"text": sodio, "answer_start": context.find(str(sodio))}]},
        {"question": "¿Cuál es el nivel de potasio del paciente?", "id": i+15, "answers": [{"text": potasio, "answer_start": context.find(str(potasio))}]},
        {"question": "¿Cuál es el nivel de cloro del paciente?", "id": i+16, "answers": [{"text": cloro, "answer_start": context.find(str(cloro))}]},
        {"question": "¿Cuál es el nivel de creatinina del paciente?", "id": i+17, "answers": [{"text": creatinina, "answer_start": context.find(str(creatinina))}]},
        {"question": "¿Cuál es el nivel de urea del paciente?", "id": i+18, "answers": [{"text": urea, "answer_start": context.find(str(urea))}]},
        {"question": "¿Cuál es el nivel de AST del paciente?", "id": i+19, "answers": [{"text": ast, "answer_start": context.find(str(ast))}]},
        {"question": "¿Cuál es el nivel de ALT del paciente?", "id": i+20, "answers": [{"text": alt, "answer_start": context.find(str(alt))}]},
        {"question": "¿Cuál es el nivel de bilirrubina del paciente?", "id": i+21, "answers": [{"text": bilirrubina, "answer_start": context.find(str(bilirrubina))}]},
        {"question": "¿Cuál es el pH del paciente?", "id": i+22, "answers": [{"text": ph, "answer_start": context.find(str(ph))}]},
        {"question": "¿Cuál es el pCO2 del paciente?", "id": i+23, "answers": [{"text": pc02, "answer_start": context.find(str(pc02))}]},
        {"question": "¿Cuál es el pO2 del paciente?", "id": i+24, "answers": [{"text": po2, "answer_start": context.find(str(po2))}]},
        {"question": "¿Cuál es el nivel de HCO3 del paciente?", "id": i+25, "answers": [{"text": hco3, "answer_start": context.find(str(hco3))}]},
        {"question": "¿Cuál es el nivel de lactato del paciente?", "id": i+26, "answers": [{"text": row['Lactato'], "answer_start": context.find(str(row['Lactato']))}]}
        ]
    
    data["data"].append({"title": titulo , "paragraphs": [{"context": context, "qas": preguntas}]})

    
    i += 10

# Guardar en JSON
with open("dataset_squad_lab_iniciales.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4,ensure_ascii=False)

print("✅ Dataset convertido a formato SQuAD.")