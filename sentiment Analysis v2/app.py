import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import gdown

# Configurar el puerto
port = int(os.environ.get("PORT", 8080))

# Mensaje de diagnóstico para confirmar que el script se está ejecutando
print(f"Starting application on port {port}")

# Enlace compartido de Google Drive (ID del archivo correcto)
file_id = '12cKhEB7WPGtZZYQ8xx9F_7XBRC_if_qt'  # Reemplaza con tu ID de archivo correcto
model_url = f'https://drive.google.com/uc?id={file_id}'
output = 'bert_model_cpu.bin'
gdown.download(model_url, output, quiet=False)

# Verifica si el archivo descargado es un modelo válido
if not os.path.exists(output) or os.path.getsize(output) < 1024:  # verifica si el archivo es muy pequeño
    raise ValueError("El archivo descargado no parece ser un modelo válido. Verifica el enlace de Google Drive.")

# Cargar el modelo y el tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Cargar el estado del modelo guardado
device = torch.device("cpu")
try:
    model.load_state_dict(torch.load(output, map_location=device))
    model.to(device)
    model.eval()
except Exception as e:
    raise ValueError(f"Error al cargar el modelo: {e}")

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definición del esquema de solicitud
class SentimentRequest(BaseModel):
    text: str

# Función de preprocesamiento
def preprocess_tweet(tweet, tokenizer, max_length=64):
    encoded_dict = tokenizer.encode_plus(
        tweet,
        add_special_tokens=True,
        max_length=max_length,
        truncation=True,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt',
    )
    return encoded_dict['input_ids'], encoded_dict['attention_mask']

# Función de predicción
def predict_tweet_sentiment(tweet, model, tokenizer):
    input_ids, attention_mask = preprocess_tweet(tweet, tokenizer)
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)
    with torch.no_grad():
        outputs = model(input_ids, token_type_ids=None, attention_mask=attention_mask)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return "Positivo" if prediction == 1 else "Negativo"

# Definir el endpoint de predicción
@app.post("/predict/")
async def predict(request: SentimentRequest):
    try:
        sentiment = predict_tweet_sentiment(request.text, model, tokenizer)
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ejecutar el servidor Uvicorn
if __name__ == "__main__":
    import uvicorn
    print(f"Running Uvicorn on host 0.0.0.0 and port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
