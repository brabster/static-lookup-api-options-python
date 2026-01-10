PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="rec-service"


gcloud run deploy rec-service-built \
  --image europe-west2-docker.pkg.dev/${PROJECT_ID}/docker/static-lookup-api-options-python:latest \
  --platform managed \
  --region europe-west2 \
  --allow-unauthenticated