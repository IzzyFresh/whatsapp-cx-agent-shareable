#!/bin/bash

# Exit immediately if any command fails
set -e

# Path to the .env file
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Error: $ENV_FILE file not found! Please ensure it exists in this directory."
  exit 1
fi

echo "🔮 Parsing environment variables from $ENV_FILE..."
# Safely parse key=value lines from .env, stripping quotes and joining with commas
ENV_VARS=$(python3 -c "
vars = []
with open('$ENV_FILE') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                k, v = line.split('=', 1)
                # Strip leading/trailing whitespaces and quotes
                k = k.strip()
                v = v.strip().strip('\"\'')
                vars.append(f'{k}={v}')
print(','.join(vars))
")

# Retrieve the GCP project ID from the .env to use for deployment configuration
PROJECT_ID=$(python3 -c "
with open('$ENV_FILE') as f:
    for line in f:
        if line.strip().startswith('GOOGLE_CLOUD_PROJECT='):
            print(line.split('=', 1)[1].strip().strip('\"\''))
")

REGION=$(python3 -c "
with open('$ENV_FILE') as f:
    for line in f:
        if line.strip().startswith('GOOGLE_CLOUD_REGION='):
            print(line.split('=', 1)[1].strip().strip('\"\''))
")

# Default region fallback if not found
if [ -z "$REGION" ]; then
  REGION="us-central1"
fi

if [ -z "$PROJECT_ID" ]; then
  echo "❌ Error: GOOGLE_CLOUD_PROJECT is not set in $ENV_FILE."
  exit 1
fi

# Map multi-region/global values to a valid single region for Cloud Run
RUN_REGION="$REGION"
if [ "$REGION" = "us" ] || [ "$REGION" = "global" ]; then
  RUN_REGION="us-central1"
  echo "⚠️  Note: GOOGLE_CLOUD_REGION is set to '$REGION' which is not a valid Cloud Run deployment region."
  echo "   Overriding deployment region to '$RUN_REGION' for Cloud Run, while keeping original env vars."
fi

echo "🚀 Deploying 'airline-example-whatsapp' to Google Cloud Run in project '$PROJECT_ID' (Region: $RUN_REGION)..."
echo "📦 Building container on Cloud Build & registering Service..."

gcloud run deploy airline-example-whatsapp \
  --source . \
  --project "$PROJECT_ID" \
  --region "$RUN_REGION" \
  --allow-unauthenticated \
  --set-env-vars "$ENV_VARS" \
  --quiet

# Retrieve the generated service URL
SERVICE_URL=$(gcloud run services describe airline-example-whatsapp --project "$PROJECT_ID" --region "$RUN_REGION" --format 'value(status.url)')

echo ""
echo "================================================================="
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "================================================================="
echo "🌍 Cloud Run Webhook URL:"
echo "   $SERVICE_URL"
echo ""
echo "⚙️  Meta Developer Console Steps:"
echo "   1. Copy the URL above."
echo "   2. Paste it as your Callback URL under WhatsApp > Configuration."
echo "   3. Verify Token remains whatever you set in WHATSAPP_VERIFY_TOKEN."
echo "   4. Test sending a message/voice note from your phone!"
echo "================================================================="
