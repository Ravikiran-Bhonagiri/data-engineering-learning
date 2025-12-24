import boto3
import json

DLQ_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/order-dlq"

def redrive_dlq():
    sqs = boto3.client('sqs', region_name='us-east-1') if False else None # Mocked
    
    print("--- Checking Dead Letter Queue (DLQ) ---")
    
    # Mock response typical of sqs.receive_message()
    messages = [
        {
            'MessageId': 'msg-1',
            'Body': json.dumps({
                "order": {"id": "o2", "amount": -50}, 
                "error": "Amount cannot be negative"
            }),
            'ReceiptHandle': 'rh1'
        },
        {
            'MessageId': 'msg-2',
            'Body': json.dumps({
                "order": {"id": "o4", "amount": 300}, 
                "error": "Missing customer_id"
            }),
            'ReceiptHandle': 'rh2'
        }
    ]
    
    if not messages:
        print("DLQ is empty.")
        return

    for msg in messages:
        payload = json.loads(msg['Body'])
        failed_order = payload['order']
        err = payload['error']
        
        print(f"\nExamining Message {msg['MessageId']}")
        print(f"Original Error: {err}")
        print(f"Payload: {failed_order}")
        
        # MANUAL INTERVENTION SIMULATION
        if "Amount cannot be negative" in err:
            print("Action: FIX -> Setting amount to absolute value.")
            failed_order['amount'] = abs(failed_order['amount'])
            print(f"Re-submitting Order {failed_order['id']} with val {failed_order['amount']}...")
            # process_order(failed_order)
            # sqs.delete_message(...)
            print("Status: REDRIVE SUCCESS ✅")
            
        elif "Missing customer_id" in err:
            print("Action: IGNORE -> Data is irretrievable.")
            print("Status: ARCHIVED TO S3 🗑️")

if __name__ == "__main__":
    redrive_dlq()
