import base64
import json

def lambda_handler(event, context):
    """
    Standard Kinesis Event Handler.
    Events come in batches.
    """
    print(f"Processing Batch of {len(event['Records'])} records...")
    
    success_count = 0
    failure_count = 0
    
    for record in event['Records']:
        try:
            # 1. Kinesis Data is Base64 Encoded
            payload_str = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            payload = json.loads(payload_str)
            
            # 2. Process Record
            process_click(payload)
            success_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to process record {record['eventID']}: {e}")
            failure_count += 1
            # In a real Stream Processor, you often want to RAISE the error
            # so the Lambda Poller knows to Bisect/Retry the batch.
            # If you just log it, the record is considered "successfully consumed" and lost.
            
            # Uncomment to demonstrate Batch Failure:
            # raise e 

    return {
        'statusCode': 200,
        'body': f"Processed {success_count} records. Failed {failure_count}."
    }

def process_click(data):
    """
    Simulated business logic.
    """
    if 'event_id' not in data:
        raise ValueError("Missing event_id")
        
    print(f" -> Ingesting Click: {data.get('url', 'Unknown')} (User: {data.get('user_id')})")

# --- Local Testing Harness ---
if __name__ == "__main__":
    # Simulating the Event Poller behavior
    print("--- Simulating Kinesis Batch ---")
    
    # 1. Create Dummy Data
    raw_data_1 = json.dumps({"event_id": "e1", "user_id": "u1", "url": "/home"})
    raw_data_2 = json.dumps({"event_id": "e2", "user_id": "u2", "url": "/cart"})
    
    # 2. Encode to Base64 (as Kinesis does)
    b64_1 = base64.b64encode(raw_data_1.encode('utf-8')).decode('utf-8')
    b64_2 = base64.b64encode(raw_data_2.encode('utf-8')).decode('utf-8')
    
    # 3. Construct Event
    mock_event = {
        "Records": [
            {"kinesis": {"data": b64_1}, "eventID": "shardId-000:1"},
            {"kinesis": {"data": b64_2}, "eventID": "shardId-000:2"}
        ]
    }
    
    lambda_handler(mock_event, None)
