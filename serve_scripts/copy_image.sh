PROJECT_ID=$(gcloud config get-value project)

docker pull ghcr.io/brabster/static-lookup-api-options-python:latest
docker image tag ghcr.io/brabster/static-lookup-api-options-python:latest europe-west2-docker.pkg.dev/${PROJECT_ID}/docker/static-lookup-api-options-python:latest 
docker push europe-west2-docker.pkg.dev/${PROJECT_ID}/docker/static-lookup-api-options-python:latest
