PROJECT_ID=$(gcloud config get-value project)
BUCKET_NAME="rec-data-${PROJECT_ID}"
SERVICE_NAME="rec-service"

gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --execution-environment gen2 \
  --add-volume name=my-gcs-vol,type=cloud-storage,bucket=${BUCKET_NAME} \
  --add-volume-mount volume=my-gcs-vol,mount-path=/mnt/gcs_data \
  --set-env-vars DB_PATH=/mnt/gcs_data/recommendations_dataset.compressed.dbm

