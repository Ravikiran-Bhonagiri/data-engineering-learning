import boto3
import json
import time
import random
import uuid
from datetime import datetime

# Stream Configuration
STREAM_NAME = "clickstream-input"
REGION = "us-east-1"

def get_kinesis_client():
    """
    Returns a boto3 client. 
    In a real scenario, this connects to AWS.
    For this portfolio demo, we wrap it to mock success if no creds are present.
    """
    try:
        return boto3.client('kinesis', region_name=REGION)
    except Exception as e:
        print(f"Warning: AWS credentials not found. Switching to Mock mode. ({e})")
        return None

def generate_click_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 100)}",
        "url": random.choice(["/home", "/cart", "/checkout", "/product/123"]),
        "timestamp": datetime.now().isoformat()
    }

def produce_records():
    client = get_kinesis_client()
    print(f"Starting Kinesis Producer for stream: {STREAM_NAME}...")

    try:
        while True:
            # 1. Generate Data
            data = generate_click_event()
            partition_key = data['user_id'] # Guarantee order per user
            
            # 2. Key Step: Put Record
            if client:
                # Real AWS Call
                # response = client.put_record(
                #     StreamName=STREAM_NAME,
                #     Data=json.dumps(data),
                #     PartitionKey=partition_key
                # )
                # print(f"Sent to ShardId: {response['ShardId']}")
                
                # Mocking the success print for portfolio demo safety
                print(f"[MOCK SEND] Pushed {data['event_id']} (PK: {partition_key})")
            else:
                 print(f"[MOCK SEND] Pushed {data['event_id']} (PK: {partition_key})")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping Producer.")

if __name__ == "__main__":
    produce_records()
