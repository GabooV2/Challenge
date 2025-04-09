#!/bin/bash

# Cargar .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️ Archivo .env no encontrado. Abortando."
  exit 1
fi

echo "🚢 Build Docker image..."
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME .

echo "📤 Pushing image..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated