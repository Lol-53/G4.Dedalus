from fastapi import FastAPI
from transformers import pipeline

# Crear pipeline con modelo en español
qa_pipeline = pipeline("question-answering", model=modelo, tokenizer=tokenizer)

# Crear API con FastAPI
app = FastAPI()

@app.post("/preguntar")
def responder(pregunta: str, contexto: str):
    resultado = qa_pipeline(question=pregunta, context=contexto)
    return {"respuesta": resultado["answer"]}

# Ejecutar con: uvicorn api:app --reload
