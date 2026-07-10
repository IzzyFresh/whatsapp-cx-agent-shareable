import os
import uuid
import logging
import google.protobuf.struct_pb2 as struct_pb2
from google.cloud import ces_v1beta

logger = logging.getLogger(__name__)

GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
CX_LOCATION = os.environ.get("CX_LOCATION", "global")
CX_AGENT_ID = os.environ.get("CX_AGENT_ID")

# Initialize CES Client
client_options = None
# Single regions containing hyphens (e.g., us-central1) require regional endpoints.
# Multi-regions (e.g., us) and global use the main global endpoint ces.googleapis.com.
if CX_LOCATION and "-" in CX_LOCATION:
    client_options = {"api_endpoint": f"{CX_LOCATION}-ces.googleapis.com"}
    
ces_client = ces_v1beta.SessionServiceClient(client_options=client_options)

def get_session_id(phone_number: str) -> str:
    """
    Deterministically map a WhatsApp phone number to a CES Session ID.
    UUID5 with a static namespace ensures the same phone number always gets the same session.
    """
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    return str(uuid.uuid5(namespace, phone_number))

def detect_intent_text(phone_number: str, text: str) -> str:
    """
    Send text to the CES Agent and get the text response.
    Injects phone_number as a session parameter so the agent can reference it.
    """
    if not CX_AGENT_ID:
        logger.error("CX_AGENT_ID environment variable is not set.")
        return "System configuration error."

    try:
        session_id = get_session_id(phone_number)
        session_path = f"projects/{GCP_PROJECT_ID}/locations/{CX_LOCATION}/apps/{CX_AGENT_ID}/sessions/{session_id}"

        config = ces_v1beta.SessionConfig(session=session_path)
        
        # Inject the phone number as a context variable for personalization
        variables = struct_pb2.Struct()
        variables.update({"phone_number": phone_number})
        
        var_input = ces_v1beta.SessionInput(variables=variables)
        text_input = ces_v1beta.SessionInput(text=text)
        
        request = ces_v1beta.RunSessionRequest(
            config=config,
            inputs=[var_input, text_input]
        )

        logger.info(f"🧠 Routing message to GCP CX Agent session {session_id}...")
        response = ces_client.run_session(request=request)
        return _extract_response_text(response)
        
    except Exception as e:
        logger.error(f"❌ GCP CX Agent call failed for phone {phone_number}: {str(e)}", exc_info=True)
        return "I'm sorry, I encountered a temporary connection issue while reaching the travel assistant. Please try again in a moment!"

def trigger_document_event(phone_number: str, gcs_uri: str, document_type: str) -> str:
    """
    Triggers a custom event in CES Agent Studio when a document is uploaded to GCS.
    Passes the GCS URI as a variable so the generative playbook can process it.
    """
    if not CX_AGENT_ID:
        logger.error("CX_AGENT_ID environment variable is not set.")
        return "System configuration error."

    try:
        session_id = get_session_id(phone_number)
        session_path = f"projects/{GCP_PROJECT_ID}/locations/{CX_LOCATION}/apps/{CX_AGENT_ID}/sessions/{session_id}"

        config = ces_v1beta.SessionConfig(session=session_path)
        
        # Create the event input
        event_name = f"DOCUMENT_UPLOADED_{document_type.upper()}" # e.g., DOCUMENT_UPLOADED_W9
        event_obj = ces_v1beta.Event(event=event_name)
        
        # Pass GCS URI and phone_number as variables
        variables = struct_pb2.Struct()
        variables.update({
            "gcs_uri": gcs_uri,
            "phone_number": phone_number
        })
        
        var_input = ces_v1beta.SessionInput(variables=variables)
        event_input = ces_v1beta.SessionInput(event=event_obj)
        
        request = ces_v1beta.RunSessionRequest(
            config=config,
            inputs=[var_input, event_input]
        )

        logger.info(f"📁 Triggering GCP Event {event_name} with URI {gcs_uri}...")
        response = ces_client.run_session(request=request)
        return _extract_response_text(response)
        
    except Exception as e:
        logger.error(f"❌ Failed to trigger GCP Event {event_name} for phone {phone_number}: {str(e)}", exc_info=True)
        return "I received your document but had trouble notifying the travel agent. Please re-upload or try again!"

def _extract_response_text(response) -> str:
    """Helper to extract the text response from a CES RunSessionResponse."""
    response_texts = []
    # response is RunSessionResponse, which has outputs (list of SessionOutput)
    for output in response.outputs:
        if output.text:
            response_texts.append(output.text)
            
    return "\n".join(response_texts) if response_texts else "..."
