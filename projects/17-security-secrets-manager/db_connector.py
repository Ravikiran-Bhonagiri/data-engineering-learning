import boto3
import json
from botocore.exceptions import ClientError

SECRET_NAME = "prod/redshift/creds"
REGION_NAME = "us-east-1"

def get_secret():
    """
    Retrieves the secret from AWS Secrets Manager.
    """
    print(f"Fetching secret '{SECRET_NAME}' from {REGION_NAME}...")
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    try:
        # 1. Network Call to AWS
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
    except ClientError as e:
        # For Portfolio Demo: Mock if AWS access fails or secret doesn't exist
        print(f"Warning: AWS Call failed ({e}). Using Mock Secret.")
        return json.dumps({
            "username": "admin",
            "password": "MOCK_PASSWORD_123",
            "engine": "redshift",
            "host": "127.0.0.1",
            "port": 5439
        })
    except Exception as e:
         # Fallback for local connection issues
         print(f"Warning: Connection failed ({e}). Using Mock Secret.")
         return json.dumps({
            "username": "admin",
            "password": "MOCK_PASSWORD_123",
            "engine": "redshift",
            "host": "127.0.0.1",
            "port": 5439
        })

    # 2. Parse the Secret String
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        # Binary secrets are returned as 'SecretBinary'
        return get_secret_value_response['SecretBinary']

def main():
    # 1. Fetch Credentials securely
    secret_str = get_secret()
    creds = json.loads(secret_str)
    
    # 2. Use Creds (Simulated DB Connection)
    print("\n--- Credential Retrieved Safely ---")
    print(f"Connecting to: {creds['host']}:{creds['port']}")
    print(f"User: {creds['username']}")
    print(f"Password: {'*' * len(creds['password'])} (Masked)")
    
    # Simulated Connection Logic
    # conn = psycopg2.connect(...)
    print("Database Connection Established!")

if __name__ == "__main__":
    main()
