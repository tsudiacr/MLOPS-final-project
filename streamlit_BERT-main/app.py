from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
import uvicorn
from multiprocessing import Process

# Carga de Modelo y Tokenizer
@torch.no_grad()
def load_model():
    tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment', force_download=True)
    model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment', force_download=True)
    model.eval()  # Asegurar que el modelo está en modo evaluación
    return tokenizer, model

tokenizer, model = load_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Definición de la clase para el input del modelo
class SentimentRequest(BaseModel):
    text: str

# Inicio de API con FastAPI
app = FastAPI()

# Endpoint para análisis de sentimientos
@app.post("/sentiment/")
def predict_sentiment(request: SentimentRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():  # Desactivar cálculo de gradientes para inferencia
            outputs = model(**inputs)
            print(f'Review: {request.text}')
            print(f'Logits: {outputs.logits}')  # Agregar esta línea para ver los logits antes de aplicar softmax
            probs = softmax(outputs.logits, dim=1)
            print(f'Probabilidades: {probs}')  # Agregar esta línea para ver las probs de cada clase

        # Devolver las probabilidades para cada una de las 5 categorías de estrellas
        return {f"{i+1}_stars": float(prob) for i, prob in enumerate(probs[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))