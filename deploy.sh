#!/bin/bash

# 1. Ask for a commit message
echo "Enter commit message (default: 'update agent logic'):"
read msg
if [ -z "$msg" ]; then
  msg="update agent logic"
fi

# 2. Sync with GitHub
echo "--- 🚀 Staging and Committing Changes ---"
git add .
git commit -m "$msg"

echo "--- ⬆️ Pushing to GitHub ---"
git push origin main

# 3. Monitor the Cloud Build
echo "--- 🛠️ Build triggered! View progress here: ---"
echo "https://console.cloud.google.com/cloud-build/builds?project=$(gcloud config get-value project)"

# 4. Provide the test command
SERVICE_URL=$(gcloud run services describe gemini-fastapi-service --platform managed --region us-central1 --format 'value(status.url)')
echo "--- ✅ Once build finishes, test with: ---"
echo "curl -X POST \"$SERVICE_URL/chat\" -H \"Content-Type: application/json\" -d '{\"name\": \"Leonardo da Vinci\"}'"
