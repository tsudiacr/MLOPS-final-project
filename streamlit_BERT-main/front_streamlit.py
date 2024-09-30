# Frontend (FE)
import requests
import streamlit as st

# Definición de la URL de la API
API_URL = "http://localhost:8000/sentiment/"

# Streamlit interface, # Configuración de la página
st.title('Análisis de sentimiento de reviews')
st.markdown('Escribe una review y obtén una calificación de "⭐" a "⭐⭐⭐⭐⭐" estrellas: \n')
review = st.text_area("Escribe tu review aquí:") # Text Area para ingreso de usuario
if st.button('Analizar review'):
    if review:
        # Preparar los datos para enviar a la API
        data = {"text": review}
        # Hacer la solicitud POST a la API
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            results = response.json()
            stars = int(max(results, key=results.get).split('_')[0])  # Split y conversión a entero
            star_display = "⭐" * stars + "☆" * (5 - stars)  # mostrar estrellas según la clasificación
            st.markdown(f"Calificación de review: {star_display} ({stars} de 5 estrellas)")
        else:
            st.error("Error en la respuesta de la API")
    else:
        st.warning("Por favor, escribe una review para analizar.")