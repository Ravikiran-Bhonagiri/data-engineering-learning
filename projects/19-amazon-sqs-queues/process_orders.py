import boto3
import json
import uuid
import random

DLQ_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/order-dlq"

def get_sqs():
    try:
        return boto3.client('sqs', region_name='us-east-1')
    except:
        return None

def send_to_dlq(order, error_msg):
    sqs = get_sqs()
    message_body = json.dumps({"order": order, "error": str(error_msg)})
    
    if sqs:
        # sqs.send_message(QueueUrl=DLQ_URL, MessageBody=message_body)
        print(f"   -> [SQS SEND] Sent to DLQ: {order['id']}")
    else:
        print(f"   -> [MOCK DLQ] Sent POISON PILL {order['id']} to Queue.")

def process_order(order):
    print(f"Processing Order {order['id']}...", end="")
    
    # Simulate Business Logic
    if order['amount'] < 0:
        raise ValueError("Amount cannot be negative")
    
    if 'customer_id' not in order:
        raise KeyError("Missing customer_id")
        
    print(" Success ✅")

def main():
    # 1. Generate Batch of Orders (Some Bad)
    orders = [
        {"id": "o1", "amount": 100, "customer_id": "c1"}, # Valid
        {"id": "o2", "amount": -50, "customer_id": "c2"}, # Invalid (Negative)
        {"id": "o3", "amount": 200, "customer_id": "c3"}, # Valid
        {"id": "o4", "amount": 300}                       # Invalid (Missing Key)
    ]
    
    print("--- Starting Batch Processing ---")
    for order in orders:
        try:
            process_order(order)
        except Exception as e:
            print(f" Failed ❌ ({e})")
            # CRITICAL PATTERN: Don't crash. Offload to DLQ.
            send_to_dlq(order, e)

if __name__ == "__main__":
    main()
