import os
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from google.cloud import storage

logger = logging.getLogger(__name__)

# Environment variables mapping for WhatsApp Business API
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "unicomer-credit-documents")
GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

# Initialize GCS client
storage_client = storage.Client(project=GCP_PROJECT_ID)

# Create a connection-pooled HTTP session with automatic backoff retries
def create_resilient_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,  # Wait 1s, 2s, 4s...
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# Shared HTTP session across all threads for high performance
http_session = create_resilient_session()

def download_whatsapp_media(media_id: str) -> tuple[bytes, str]:
    """
    Downloads media from WhatsApp servers given a media ID.
    Meta uses a 2-step process:
    1. Retrieve the media URL using the media ID.
    2. Download the binary data from the media URL using the Bearer token.
    """
    if not WHATSAPP_TOKEN:
        raise ValueError("WHATSAPP_TOKEN environment variable is not set.")

    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    # Step 1: Get media URL
    media_info_url = f"https://graph.facebook.com/v18.0/{media_id}"
    logger.info(f"📥 Fetching WhatsApp media metadata for ID {media_id}...")
    response = http_session.get(media_info_url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch media info: {response.text}")
        raise Exception("Failed to fetch media metadata from WhatsApp.")

    media_data = response.json()
    download_url = media_data.get("url")
    mime_type = media_data.get("mime_type")

    # Step 2: Download the actual binary payload
    logger.info(f"📥 Downloading binary payload from Meta CDN...")
    media_response = http_session.get(download_url, headers=headers)
    if media_response.status_code != 200:
        logger.error(f"Failed to download media binary: {media_response.text}")
        raise Exception("Failed to download media binary from WhatsApp.")

    return media_response.content, mime_type

def upload_to_gcs(binary_data: bytes, phone_number: str, media_id: str, mime_type: str) -> str:
    """
    Uploads the raw binary media to a secure, hierarchical GCS structure.
    """
    try:
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        
        # Determine strict extension based on mime type mapping
        extension = ".bin"
        if "jpeg" in mime_type or "jpg" in mime_type:
            extension = ".jpg"
        elif "png" in mime_type:
            extension = ".png"
        elif "pdf" in mime_type:
            extension = ".pdf"
        elif "ogg" in mime_type or "opus" in mime_type:
            extension = ".ogg"
        elif "aac" in mime_type:
            extension = ".aac"
        elif "audio" in mime_type:
            extension = ".wav"
            
        # Determine logical folder based on file type for easier lifecycle management
        folder = "images" if "image" in mime_type else ("documents" if "pdf" in mime_type else ("audio" if "audio" in mime_type else "misc"))
        
        # Build deterministic path: gs://bucket/phone/type/id.ext
        destination_blob_name = f"uploads/{phone_number}/{folder}/{media_id}{extension}"
        blob = bucket.blob(destination_blob_name)
        
        # Upload from memory
        blob.upload_from_string(binary_data, content_type=mime_type)
        logger.info(f"Successfully uploaded media to gs://{GCS_BUCKET_NAME}/{destination_blob_name}")
        
        # Return the GCS URI which can be passed to Document AI or BigQuery
        return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"
        
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {str(e)}")
        raise e

def send_whatsapp_message(to: str, message_body: str) -> dict:
    """
    Sends a text message back to the user via WhatsApp Business API.
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        logger.error("WhatsApp credentials missing. Cannot send message.")
        return {}
        
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message_body}
    }

    logger.info(f"📤 Sending outbound reply to {to}...")
    response = http_session.post(url, headers=headers, json=payload)
    if response.status_code != 200:
         logger.error(f"Failed to send WhatsApp message: {response.text}")
    return response.json()
