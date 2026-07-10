import os
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
DATASET_ID = os.environ.get("BQ_DATASET", "copa_airline_demo")

def setup_bigquery():
    client = bigquery.Client(project=PROJECT_ID)
    
    # 1. Create Dataset
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    try:
        dataset = client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset.dataset_id} created or already exists.")
    except Exception as e:
        print(f"Error creating dataset: {e}")

    # 2. Define Passports Table Schema
    passports_schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("file", "STRING"),
        bigquery.SchemaField("first_name", "STRING"),
        bigquery.SchemaField("last_name", "STRING"),
        bigquery.SchemaField("passport_number", "STRING"),
        bigquery.SchemaField("nationality", "STRING"),
        bigquery.SchemaField("date_of_birth", "STRING"),
        bigquery.SchemaField("expiration_date", "STRING"),
    ]
    
    passports_table_ref = f"{dataset_ref}.passports"
    passports_table = bigquery.Table(passports_table_ref, schema=passports_schema)
    
    try:
        client.create_table(passports_table, exists_ok=True)
        print(f"Table {passports_table.table_id} created or already exists.")
    except Exception as e:
        print(f"Error creating table passports: {e}")
        
    # 3. Define Tickets Table Schema
    tickets_schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("file", "STRING"),
        bigquery.SchemaField("passenger_name", "STRING"),
        bigquery.SchemaField("airline", "STRING"),
        bigquery.SchemaField("flight_number", "STRING"),
        bigquery.SchemaField("origin", "STRING"),
        bigquery.SchemaField("destination", "STRING"),
        bigquery.SchemaField("departure_date", "STRING"),
        bigquery.SchemaField("seat", "STRING"),
    ]
    
    tickets_table_ref = f"{dataset_ref}.tickets"
    tickets_table = bigquery.Table(tickets_table_ref, schema=tickets_schema)
    
    try:
        client.create_table(tickets_table, exists_ok=True)
        print(f"Table {tickets_table.table_id} created or already exists.")
    except Exception as e:
        print(f"Error creating table tickets: {e}")

    # 4. Define Baggage Logs Table Schema
    baggage_schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("file", "STRING"),
        bigquery.SchemaField("passenger_name", "STRING"),
        bigquery.SchemaField("baggage_tag", "STRING"),
        bigquery.SchemaField("damage_description", "STRING"),
        bigquery.SchemaField("estimated_value", "STRING"),
    ]
    
    baggage_table_ref = f"{dataset_ref}.baggage_logs"
    baggage_table = bigquery.Table(baggage_table_ref, schema=baggage_schema)
    
    try:
        client.create_table(baggage_table, exists_ok=True)
        print(f"Table {baggage_table.table_id} created or already exists.")
    except Exception as e:
        print(f"Error creating table baggage_logs: {e}")

if __name__ == "__main__":
    setup_bigquery()
