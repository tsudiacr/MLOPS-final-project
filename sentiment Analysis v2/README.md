https://www.youtube.com/watch?v=J0y2tjBz2Ao&ab_channel=Garajedeideas%7CTech


**#Paso 1**
#python3 -m venv fastapi-env

source fastapi-env/bin/activate

pip install fastapi

pip install streamlit    

pip install torch    

pip install transformers 

pip install -r requirements.txt


**#Paso 2 para ejecutar**
uvicorn main:app --reload

**#Paso 3 Docker**
3.1 Tener instalado Docker en la computadora.  
3.2 Abrir la app de docker.  
3.3 sudo docker build -t sentiment-analysis-api .  
3.4 docker run -p 8000:8000 sentiment-analysis-api  



**Paso #4 Probar en Postman**
4.1 Crear un nuevo tab.  
4.2 Escoger POST.  
4.3 escribir el url : http://0.0.0.0:8080/predict/  
4.4 en los Header escribir : key= Content-Type type = application/json  
4.5 Body Raw Json   

{
    "text": "the elections were the best"
}

**Paso #5 Desplegar en Docker Hub**
5.1 (fastapi-env) dianagonzalez@MacBook-Pro fastAPI % sudo docker build -t sentiment-analysis-api .  
5.2 (fastapi-env) dianagonzalez@MacBook-Pro fastAPI % docker push dianmelis/sentiment-analysis-api:latest    
5.3 https://hub.docker.com/r/dianmelis/sentiment-analysis-api


**Paso# 6 Opcional**
**Instalar gcloud**
brew install --cask google-cloud-sdk
gcloud version
gcloud info
gcloud auth list
gcloud services enable artifactregistry.googleapis.com

**Crear repositorio en GCloud**
gcloud artifacts repositories create sentimentanalysisapi-local \
    --repository-format=docker \
    --location=us-central1 \
    --description="Local Docker repository for sentiment analysis API"


6.1 gcloud auth configure-docker us-central1-docker.pkg.dev  
6.2 sudo docker build -t sentiment-analysis-api .  
6.3 sudo docker tag sentiment-analysis-api us-central1-docker.pkg.dev/ml-analisis-de-sentimientos/sentimentanalysisapi-local/sentiment-analysis-api:latest  
6.4 docker push us-central1-docker.pkg.dev/ml-analisis-de-sentimientos/sentimentanalysisapi-local/sentiment-analysis-api:latest  

*Pasar de dockerHub a Google*  
docker tag your_dockerhub_username/sentiment-analysis-api:latest \
us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/[REPOSITORY_NAME]/sentiment-analysis-api:latest  


**Paso #7 Opcional Cloud Run**
sudo docker build --platform linux/amd64 -t sentiment-analysis-api .

sudo docker tag sentiment-analysis-api us-central1-docker.pkg.dev/ml-analisis-de-sentimientos/sentimentanalysisapi-local/sentiment-analysis-api:latest

sudo docker push us-central1-docker.pkg.dev/ml-analisis-de-sentimientos/sentimentanalysisapi-local/sentiment-analysis-api:latest

gcloud run deploy sentiment-analysis-api \
    --image us-central1-docker.pkg.dev/ml-analisis-de-sentimientos/sentimentanalysisapi-local/sentiment-analysis-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi


    URL: https://sentiment-analysis-api-5hkvjt4p3q-uc.a.run.app/predict/
    
