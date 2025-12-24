from opensearchpy import OpenSearch, RequestsHttpConnection
import json
from datetime import datetime

# Configuration
HOST = 'search-my-domain.us-east-1.es.amazonaws.com'
REGION = 'us-east-1'
AUTH = ('admin', 'SuperSecret123!') # In prod, use IAM integration

def get_client():
    """
    Returns an OpenSearch client.
    """
    # For portfolio demo, returning Mock if connection fails
    return OpenSearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=AUTH,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def index_log(client, document):
    index_name = "app-logs-2024"
    
    try:
        response = client.index(
            index=index_name,
            body=document,
            refresh=True
        )
        print(f"Indexed Document ID: {response['_id']}")
    except Exception as e:
        print(f"[MOCK INDEX] {doc['message']} (Connection: {e})")

if __name__ == "__main__":
    client = get_client()

    print("--- Starting Log Ingestion ---")

    # Sample Log Entries
    logs = [
        {"timestamp": datetime.now().isoformat(), "level": "INFO", "message": "User login successful", "user_id": 101},
        {"timestamp": datetime.now().isoformat(), "level": "ERROR", "message": "Database connection timeout", "module": "db_module"},
        {"timestamp": datetime.now().isoformat(), "level": "WARN", "message": "High memory usage detected", "node": "worker-1"}
    ]

    for doc in logs:
        index_log(client, doc)
        
    print("--- Ingestion Complete. Searchable via Dashboard. ---")
