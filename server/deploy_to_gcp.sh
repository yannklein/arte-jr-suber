# from the dropdown at the top of Cloud Console:
export GCLOUD_PROJECT="arte-jr-subber" 
# from Step 2.2 above:
export REPO="arte-jr-subber-repository"
# the region you chose in Step 2.4:
export REGION="europe-west1"
# whatever you want to call this image:
export IMAGE="arte-jr-subber-project-image"

# use the region you chose above here in the URL:
export IMAGE_TAG=${REGION}-docker.pkg.dev/$GCLOUD_PROJECT/$REPO/$IMAGE

# Build the image:
docker build -t $IMAGE_TAG -f /Users/kleinyann/github/arte-jr-suber/server/Dockerfile --platform linux/x86_64 .
# Push it to Artifact Registry:
docker push $IMAGE_TAG