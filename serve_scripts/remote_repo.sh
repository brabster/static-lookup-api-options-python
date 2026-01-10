PROJECT_ID=$(gcloud config get-value project)

gcloud artifacts repositories create ghcr \
  --project=${PROJECT_ID} \
  --repository-format=docker \
  --location=europe-west2 \
  --description=ghcr.io \
  --mode=remote-repository \
  --remote-repo-config-desc="GitHub Container Repository" \
  --remote-docker-repo=https://ghcr.io
