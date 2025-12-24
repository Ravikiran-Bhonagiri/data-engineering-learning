import json

def lambda_handler(event, context):
    """
    Triggered by DynamoDB Stream.
    Event contains a list of 'Records'.
    """
    print(f"Received batch of {len(event['Records'])} change events.")
    
    for record in event['Records']:
        try:
            event_name = record['eventName'] # INSERT, MODIFY, REMOVE
            
            # DynamoDB Stream record includes Keys
            pk = record['dynamodb']['Keys']['PK']['S']
            sk = record['dynamodb']['Keys']['SK']['S']
            
            print(f"--- Processing {event_name} for {pk} / {sk} ---")
            
            if event_name == 'INSERT':
                new_image = record['dynamodb']['NewImage']
                handle_insert(new_image)
                
            elif event_name == 'MODIFY':
                old_image = record['dynamodb']['OldImage']
                new_image = record['dynamodb']['NewImage']
                handle_modify(old_image, new_image)
                
            elif event_name == 'REMOVE':
                print("Item deleted. Performing cleanup...")

        except Exception as e:
            print(f"Error processing record: {e}")
            # In production, we would Raise here to trigger Lambda Retry/DLQ
            
    return "Successfully processed records."

def handle_insert(new_image):
    """
    Logic for new items.
    Example: Send Welcome Email or Index in Search.
    """
    # Unpack DynamoDB JSON format ( e.g. {'S': 'some val'} )
    # Using a helper would be cleaner, but keeping raw for visibility
    if 'email' in new_image:
        email = new_image['email']['S']
        print(f" [ACTION] Sending Welcome Email to: {email}")

def handle_modify(old_image, new_image):
    """
    Logic for updates.
    Example: Audit Logging logic.
    """
    print(" [ACTION] Audit Log: Detected change.")
    
    # Check what changed
    if 'status' in old_image and 'status' in new_image:
        old_status = old_image['status']['S']
        new_status = new_image['status']['S']
        if old_status != new_status:
            print(f"   -> Status changed from '{old_status}' to '{new_status}'")

# --- Local Testing Harness ---
if __name__ == "__main__":
    with open('test_stream_event.json', 'r') as f:
        mock_event = json.load(f)
    
    lambda_handler(mock_event, None)
