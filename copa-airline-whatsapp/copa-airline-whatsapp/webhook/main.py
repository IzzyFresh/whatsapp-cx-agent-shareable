import os
import json
import hmac
import hashlib
import logging
import threading
from collections import deque
import functions_framework
from flask import Request, Response
from dotenv import load_dotenv

# Load environment variables from the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

from google import genai
from google.genai import types
from whatsapp_client import download_whatsapp_media, upload_to_gcs, send_whatsapp_message
from cx_client import detect_intent_text, trigger_document_event

# Setup professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GenAI Client for audio transcription
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

# Map location to valid endpoints for the newer Google GenAI SDK
sdk_location = LOCATION
if LOCATION == "us" or LOCATION == "global":
    sdk_location = "global"

ai_client = genai.Client(enterprise=True, project=PROJECT_ID, location=sdk_location)

def transcribe_audio_gcs(gcs_uri: str, mime_type: str) -> str:
    """Uses Gemini 2.5 Flash to transcribe the audio voice note directly from GCS."""
    logger.info(f"🎙️ Transcribing voice note from {gcs_uri} using {MODEL_ID}...")
    audio_part = types.Part.from_uri(file_uri=gcs_uri, mime_type=mime_type)
    
    response = ai_client.models.generate_content(
        model=MODEL_ID,
        contents=[audio_part, "Please transcribe this audio file accurately. Return only the transcription text without any introductory or concluding words."]
    )
    return response.text.strip()

# Verify Token for WhatsApp Webhook subscription verification
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "YOUR_WHATSAPP_VERIFY_TOKEN")
APP_SECRET = os.environ.get("WHATSAPP_APP_SECRET")

# Thread-safe in-memory cache to prevent duplicate processing of Meta webhooks (3s retry window)
PROCESSED_MESSAGE_IDS = set()
PROCESSED_IDS_DEQUE = deque()
cache_lock = threading.Lock()
MAX_CACHE_SIZE = 1000

def is_duplicate_message(message_id: str) -> bool:
    """Check if message_id is duplicate in a thread-safe sliding cache."""
    if not message_id:
        return False
    with cache_lock:
        if message_id in PROCESSED_MESSAGE_IDS:
            return True
        PROCESSED_MESSAGE_IDS.add(message_id)
        PROCESSED_IDS_DEQUE.append(message_id)
        # Prune oldest element when cache limit is exceeded
        if len(PROCESSED_IDS_DEQUE) > MAX_CACHE_SIZE:
            oldest = PROCESSED_IDS_DEQUE.popleft()
            PROCESSED_MESSAGE_IDS.discard(oldest)
        return False

def verify_signature(request: Request) -> bool:
    """Verifies that the incoming request payload comes securely from Meta using SHA256 HMAC."""
    if not APP_SECRET:
        logger.warning("⚠️ WHATSAPP_APP_SECRET is not configured. Skipping signature verification (Development Mode).")
        return True
        
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header or not signature_header.startswith("sha256="):
        logger.warning("❌ Security alert: Missing or malformed X-Hub-Signature-256 header.")
        return False
        
    received_signature = signature_header.split("sha256=")[1]
    payload = request.get_data()
    
    expected_signature = hmac.new(
        APP_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, received_signature)

@functions_framework.http
def whatsapp_webhook(request: Request) -> Response:
    """
    HTTP Cloud Function handling the secure WhatsApp Business API Webhook.
    """
    if request.method == 'GET':
        # WhatsApp Webhook Verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                logger.info("✅ WEBHOOK_VERIFIED successfully")
                return Response(challenge, status=200)
            else:
                logger.warning(f"❌ Webhook verification failed. Received token: '{token}' does not match expected VERIFY_TOKEN.")
                return Response('Forbidden', status=403)
        return Response('Bad Request', status=400)

    elif request.method == 'POST':
        # Security validation
        if not verify_signature(request):
            return Response('Unauthorized Signature', status=401)

        try:
            body = request.get_json()
            if not body or body.get('object') != 'whatsapp_business_account':
                return Response('Not a WhatsApp Event', status=404)

            for entry in body.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    if 'messages' in value:
                        message = value['messages'][0]
                        message_id = message.get('id')
                        sender_phone = message.get('from')
                        
                        # Apply thread-safe deduplication
                        if is_duplicate_message(message_id):
                            logger.info(f"🔄 Webhook deduplication triggered. Skipping duplicate message ID: {message_id}")
                            return Response('EVENT_RECEIVED (DEDUPLICATED)', status=200)
                        
                        # 1. Handle Text Messages
                        if 'text' in message:
                            text_body = message['text']['body']
                            logger.info(f"📲 Received WhatsApp text from {sender_phone}: {text_body}")
                            
                            # Route text input to Conversational Agent
                            reply = detect_intent_text(sender_phone, text_body)
                            
                            # Send response back to user
                            send_whatsapp_message(sender_phone, reply)
                            
                        # 2. Handle Images (e.g. Passport/Luggage upload)
                        elif 'image' in message:
                            media_id = message['image']['id']
                            logger.info(f"📸 Received WhatsApp image from {sender_phone} with Media ID: {media_id}")
                            
                            # Download from Meta CDN
                            binary_data, mime_type = download_whatsapp_media(media_id)
                            # Upload to secure GCS bucket
                            gcs_uri = upload_to_gcs(binary_data, sender_phone, media_id, mime_type)
                            # Trigger "DOCUMENT_UPLOADED_IMAGE" custom agent event
                            reply = trigger_document_event(sender_phone, gcs_uri, "IMAGE")
                            
                            # Send reply back to user
                            send_whatsapp_message(sender_phone, reply)
                            
                        # 3. Handle Documents (e.g. Booking confirmations / PDF Tickets)
                        elif 'document' in message:
                            media_id = message['document']['id']
                            logger.info(f"📄 Received WhatsApp document from {sender_phone} with Media ID: {media_id}")
                            
                            # Download from Meta CDN
                            binary_data, mime_type = download_whatsapp_media(media_id)
                            # Upload to secure GCS bucket
                            gcs_uri = upload_to_gcs(binary_data, sender_phone, media_id, mime_type)
                            # Trigger "DOCUMENT_UPLOADED_DOCUMENT" custom agent event
                            reply = trigger_document_event(sender_phone, gcs_uri, "DOCUMENT")
                            
                            # Send reply back to user
                            send_whatsapp_message(sender_phone, reply)
                            
                        # 4. Handle Voice Notes / Audio messages (GenAI Transcription)
                        elif 'audio' in message:
                            media_id = message['audio']['id']
                            logger.info(f"🎙️ Received WhatsApp voice note from {sender_phone} with Media ID: {media_id}")
                            
                            # Download from Meta CDN
                            binary_data, mime_type = download_whatsapp_media(media_id)
                            # Upload to secure GCS bucket
                            gcs_uri = upload_to_gcs(binary_data, sender_phone, media_id, mime_type)
                            # Transcribe with Gemini 3.5 Flash
                            transcription = transcribe_audio_gcs(gcs_uri, mime_type)
                            logger.info(f"🎙️ Transcribed voice note text: \"{transcription}\"")
                            
                            if transcription:
                                # Route text input to Conversational Agent
                                reply = detect_intent_text(sender_phone, transcription)
                                # Send response back to user
                                send_whatsapp_message(sender_phone, reply)
                            else:
                                logger.warning("⚠️ Transcription was empty.")
                            
            return Response('EVENT_RECEIVED', status=200)
            
        except Exception as e:
            logger.error(f"❌ Error processing webhook message: {str(e)}", exc_info=True)
            return Response("Internal Error", status=500)
            
    return Response('Method not allowed', status=405)
