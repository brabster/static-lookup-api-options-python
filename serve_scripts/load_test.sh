FUSE_URL=https://rec-service-1006445885426.europe-west1.run.app/
BUILT_URL=https://rec-service-built-1006445885426.europe-west2.run.app/

locust --headless -f load_test.py --host=${BUILT_URL} -u 20 --run-time 3m
