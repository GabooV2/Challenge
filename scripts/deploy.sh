#!/bin/bash

# Cargar variables de entorno desde el archivo .env
set -o allexport
source .env
set +o allexport

# Validar que gcloud esté instalado
if ! command -v gcloud &> /dev/null; then
    echo "gcloud no está instalado. Instalalo con: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "Build Docker image..."
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME .

echo "Pushing image..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME

echo "Deploying to Cloud Run Job..."
gcloud run jobs create scraper-job \
  --image=southamerica-east1-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME \
  --region=southamerica-east1 \
  --command="python" \
  --args="main.py" \
  --project=$PROJECT_ID

echo "Executing the job..."
gcloud run jobs execute scraper-job --region=$REGION

