import json
import boto3
import urllib.parse
from datetime import datetime

# Initialize clients outside handler for reuse (Warm Starts)
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileMetadata')

def lambda_handler(event, context):
    """
    Standard AWS Lambda entry point.
    """
    print("Received event: " + json.dumps(event, indent=2))

    # Loop through every record in the S3 event (usually just one)
    for record in event['Records']:
        # 1. Extract Bucket and Key
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        
        try:
            # 2. Get File Metadata (Head Object) - Simulation
            # In a real environment, we would call:
            # response = s3.head_object(Bucket=bucket, Key=key)
            # size = response['ContentLength']
            
            # Simulating size for local run
            size = 1024 
            print(f"Processing content of {key} from {bucket}")

            # 3. Write Metadata to DynamoDB
            # We use the S3 Key as the Primary ID
            item = {
                'file_id': key,
                'bucket_name': bucket,
                'size_bytes': size,
                'timestamp': datetime.now().isoformat(),
                'status': 'PROCESSED'
            }
            
            # In real environment:
            # table.put_item(Item=item)
            print(f"--- [MOCK WRITE TO DYNAMODB] ---\n{json.dumps(item, indent=2)}")

        except Exception as e:
            print(e)
            print(f"Error getting object {key} from bucket {bucket}.")
            raise e
            
    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully!')
    }

# --- Local Testing Harness ---
if __name__ == "__main__":
    # Load the mock event
    with open('test_event.json', 'r') as f:
        mock_event = json.load(f)
    
    # Run the handler
    lambda_handler(mock_event, None)
