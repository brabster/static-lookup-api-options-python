PROJECT_ID=$(gcloud config get-value project)
BUCKET_NAME="rec-data-${PROJECT_ID}"
SERVICE_NAME="rec-service"

gcloud run deploy ${SERVICE_NAME} \
  --image europe-west2-docker.pkg.dev/${PROJECT_ID}/docker/static-lookup-api-options-python:latest \
  --platform managed \
  --region europe-west2 \
  --execution-environment gen2 \
  --scaling 1 \
  --command gunicorn \
  --args='--bind,:8080,--workers,3,app:app' \
  --allow-unauthenticated \
  --add-volume name=my-gcs-vol,type=cloud-storage,bucket=${BUCKET_NAME} \
  --add-volume-mount volume=my-gcs-vol,mount-path=/mnt/gcs_data \
  --set-env-vars DB_PATH=/mnt/gcs_data/recommendations_dataset.compressed.dbm
  