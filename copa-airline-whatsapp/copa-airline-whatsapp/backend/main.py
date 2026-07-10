import os
import time
import json
import base64
import logging
import mimetypes
import functions_framework
from google import genai
from google.genai import types
from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
BQ_DATASET = os.environ.get("BQ_DATASET", "copa_airline_demo")
MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
GCS_BUCKET = os.environ.get("GCS_BUCKET_NAME", "YOUR_GCS_BUCKET_NAME")

# Map multi-region location to valid Vertex AI endpoints
vertexai_location = LOCATION
if LOCATION == "us":
    if "3.5" in MODEL_ID:
        vertexai_location = "global"
    else:
        vertexai_location = "us-central1"

# Initialize Clients
bq_client = bigquery.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)
ai_client = genai.Client(enterprise=True, project=PROJECT_ID, location=vertexai_location)

def get_mime_type(uri_or_path: str) -> str:
    """Guess mime-type based on file extension, defaulting to image/jpeg."""
    mime_type, _ = mimetypes.guess_type(uri_or_path)
    if not mime_type:
        if uri_or_path.lower().endswith('.pdf'):
            mime_type = 'application/pdf'
        elif uri_or_path.lower().endswith('.png'):
            mime_type = 'image/png'
        else:
            mime_type = 'image/jpeg'
    return mime_type

def process_with_gemini_gcs(gcs_uri: str, mime_type: str, extraction_prompt: str, json_schema: dict) -> dict:
    """Uses Gemini to parse a document using its GCS URI directly."""
    logger.info(f"Extracting data using GCS GenAI processing from {gcs_uri} with {MODEL_ID}")
    
    # Efficient native storage-to-GenAI linkage via from_uri
    document_part = types.Part.from_uri(file_uri=gcs_uri, mime_type=mime_type)
    
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=json_schema,
        temperature=0.1
    )
    
    response = ai_client.models.generate_content(
        model=MODEL_ID,
        contents=[document_part, extraction_prompt],
        config=config
    )
    
    try:
        extracted_data = json.loads(response.text)
        return extracted_data
    except Exception as e:
        logger.error(f"Failed to parse Gemini output as JSON. Output was: {response.text}")
        raise e

def insert_into_bigquery(table_name: str, extracted_data: dict, gcs_uri: str):
    """Inserts structured data into BigQuery by matching dictionary keys to table columns."""
    table_ref = bq_client.dataset(BQ_DATASET).table(table_name)
    table = bq_client.get_table(table_ref)
    
    valid_columns = [field.name for field in table.schema]
    
    doc_row = {}
    for k, v in extracted_data.items():
        normalized_key = k.lower().replace(" ", "").replace("_", "")
        
        matched_col = next((col for col in valid_columns if col.lower().replace("_", "") == normalized_key), None)
        if matched_col:
            doc_row[matched_col] = str(v)

    if 'id' in valid_columns:
        doc_row['id'] = f"copa-upload-{int(time.time())}"
    if 'file' in valid_columns:
        doc_row['file'] = gcs_uri
        
    errors = bq_client.insert_rows_json(table, [doc_row])
    if errors:
        logger.error(f"BigQuery Insert Errors: {errors}")
        raise Exception(f"Failed to insert into BQ: {errors}")
        
    logger.info(f"Successfully inserted record into {table_name}")

def save_to_gcs(base64_data: str, phone_number: str, doc_category: str) -> tuple[str, str]:
    """Decodes Base64 data and saves it to the hierarchical GCS bucket."""
    bucket = storage_client.bucket(GCS_BUCKET)
    timestamp = int(time.time())
    
    extension = "pdf" if doc_category == "tickets" else "jpg"
    mime_type = "application/pdf" if doc_category == "tickets" else "image/jpeg"
    
    blob_name = f"{phone_number}/{doc_category}/{timestamp}_{doc_category}.{extension}"
    blob = bucket.blob(blob_name)
    
    image_bytes = base64.b64decode(base64_data)
    blob.upload_from_string(image_bytes, content_type=mime_type)
    
    gcs_uri = f"gs://{GCS_BUCKET}/{blob_name}"
    logger.info(f"Saved uploaded document to GCS: {gcs_uri}")
    return gcs_uri, mime_type

@functions_framework.http
def process_document_upload(request):
    """
    HTTP Cloud Function triggered by Dialogflow CX OpenAPI Tool or webhook flows.
    Expects a JSON payload with either a GCS URI ('gcs_uri') or Base64 encoded document ('document').
    """
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        return {"status": "error", "message": "Missing JSON payload."}, 400
        
    payload = request_json
    # Handle Dialogflow CX double-encoded stringification wrapping
    if 'upload_document' in request_json:
        payload = request_json['upload_document']
        
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
            if isinstance(payload, str):
                payload = json.loads(payload)
        except Exception as e:
            return {"status": "error", "message": f"Failed to deserialize string payload: {str(e)}"}, 400

    gcs_uri = payload.get('gcs_uri')
    base64_doc = payload.get('document')
    doc_type = payload.get('doc_type', '').upper()
    phone_number = payload.get('phone_number', 'unknown_user')

    if not gcs_uri and not base64_doc:
        return {"status": "error", "message": "Missing document source. Provide either 'gcs_uri' or 'document' (Base64)."}, 400

    if not doc_type:
        return {"status": "error", "message": "Missing required field: 'doc_type'"}, 400

    try:
        if doc_type in ['PASSPORT', 'DL']:
            logger.info("Routing upload to Passport Parser")
            if gcs_uri:
                mime_type = get_mime_type(gcs_uri)
            else:
                gcs_uri, mime_type = save_to_gcs(base64_doc, phone_number, "passports")
            
            schema = {
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "passport_number": {"type": "string"},
                    "nationality": {"type": "string"},
                    "date_of_birth": {"type": "string"},
                    "expiration_date": {"type": "string"}
                },
                "required": ["first_name", "last_name", "passport_number"]
            }
            prompt = "Extract the first name, last name, passport number, nationality, date of birth, and expiration date from this passport identification document."
            extracted = process_with_gemini_gcs(gcs_uri, mime_type, prompt, schema)
            insert_into_bigquery('passports', extracted, gcs_uri)
            
            return {
                "status": "success",
                "message": "Passport captured and processed successfully.",
                "extracted": extracted,
                "file_uri": gcs_uri
            }, 200
            
        elif doc_type in ['TICKET', 'BOARDING_PASS', 'PAYSTUB']:
            logger.info("Routing upload to Ticket/Boarding Pass Parser")
            if gcs_uri:
                mime_type = get_mime_type(gcs_uri)
            else:
                gcs_uri, mime_type = save_to_gcs(base64_doc, phone_number, "tickets")
            
            schema = {
                "type": "object",
                "properties": {
                    "passenger_name": {"type": "string"},
                    "airline": {"type": "string"},
                    "flight_number": {"type": "string"},
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "seat": {"type": "string"}
                },
                "required": ["passenger_name", "flight_number"]
            }
            prompt = "Extract the passenger name, airline, flight number, origin city/airport, destination city/airport, departure date, and seat number from this boarding pass or ticket confirmation."
            extracted = process_with_gemini_gcs(gcs_uri, mime_type, prompt, schema)
            insert_into_bigquery('tickets', extracted, gcs_uri)
            
            return {
                "status": "success",
                "message": "Ticket/Boarding pass processed successfully.",
                "extracted": extracted,
                "file_uri": gcs_uri
            }, 200
            
        elif doc_type in ['BAGGAGE', 'BANK_STATEMENT']:
            logger.info("Routing upload to Baggage Damage/Log Parser")
            if gcs_uri:
                mime_type = get_mime_type(gcs_uri)
            else:
                gcs_uri, mime_type = save_to_gcs(base64_doc, phone_number, "baggage")
            
            schema = {
                "type": "object",
                "properties": {
                    "passenger_name": {"type": "string"},
                    "baggage_tag": {"type": "string"},
                    "damage_description": {"type": "string"},
                    "estimated_value": {"type": "string"}
                },
                "required": ["passenger_name"]
            }
            prompt = ("Extract the passenger name and baggage tag number from this bag tag or photo. "
                      "If the image depicts damaged baggage, describe the damage and estimate repair cost or value if indicated; otherwise, provide empty values for damage_description and estimated_value.")
            extracted = process_with_gemini_gcs(gcs_uri, mime_type, prompt, schema)
            insert_into_bigquery('baggage_logs', extracted, gcs_uri)
            
            return {
                "status": "success",
                "message": "Baggage claim/damage photo processed successfully.",
                "extracted": extracted,
                "file_uri": gcs_uri
            }, 200
            
        else:
            return {"status": "error", "message": f"Unsupported doc_type: {doc_type}"}, 400
            
    except Exception as e:
        logger.error(f"Failed to process document upload: {str(e)}")
        return {"status": "error", "message": f"Internal Processing Error: {str(e)}"}, 500
