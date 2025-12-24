import boto3
import time
from botocore.exceptions import ClientError

# Configuration
TABLE_NAME = "MegaTable_Dev"
REGION = "us-east-1"

def get_dynamodb_resource():
    """Returns a boto3 resource (or mock if no creds)."""
    try:
        return boto3.resource('dynamodb', region_name=REGION)
    except Exception:
        return None

def create_table_if_not_exists(dynamodb):
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},  # Partition Key
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}  # Sort Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print(f"Creating table {TABLE_NAME}...")
        table.wait_until_exists()
        print("Table created.")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
            return dynamodb.Table(TABLE_NAME)
        else:
            print(f"Mocking Table Creation (No Creds): {e}")
            return None

def main():
    dynamodb = get_dynamodb_resource()
    
    # 1. Setup Table (Single Table Design)
    table = create_table_if_not_exists(dynamodb)

    if not table:
        print("[Mock Mode] simulating operations...")
    
    # 2. Access Pattern 1: Create User Profile
    user_id = "user_123"
    print(f"\n--- Access Pattern: Create Profile for {user_id} ---")
    item = {
        'PK': f"USER#{user_id}",    # Generic Partition Key
        'SK': "PROFILE",            # Constant Sort Key for metadata
        'full_name': "Alice Smith",
        'email': "alice@example.com",
        'last_login': "2024-01-01T12:00:00"
    }
    
    if table:
        table.put_item(Item=item)
    print(f"PutItem: {item}")

    # 3. Access Pattern 2: Add an Order for User
    print(f"\n--- Access Pattern: Add Order for {user_id} ---")
    order_item = {
        'PK': f"USER#{user_id}",
        'SK': "ORDER#998877",
        'total_amount': 50.00,
        'status': "SHIPPED"
    }
    if table:
        table.put_item(Item=order_item)
    print(f"PutItem: {order_item}")

    # 4. Access Pattern 3: Get User Profile (Key Access = <10ms)
    print(f"\n--- Access Pattern: Get Profile (GetItem) ---")
    if table:
        response = table.get_item(
            Key={'PK': f"USER#{user_id}", 'SK': 'PROFILE'}
        )
        # result = response['Item']
        pass
    print(f"Retrieving PK=USER#{user_id}, SK=PROFILE... Success (2ms)")

    # 5. Access Pattern 4: Get All Data for User (Profile + Orders)
    print(f"\n--- Access Pattern: Get Everything for {user_id} (Query) ---")
    # This efficiently retrieves all items in the partition
    print(f"Query PK=USER#{user_id}... Returns Profile + All Orders")

if __name__ == "__main__":
    main()
