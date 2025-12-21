# Advanced & Niche Services 🎯

[← Back to Main](../README.md)

Services you may not use daily, but are invaluable for specific use cases.

---

## [AWS DataSync](https://aws.amazon.com/datasync/)

Automate and accelerate moving data between on-premises storage and AWS storage services.

- **Why it matters:** When you need to migrate terabytes/petabytes from on-prem to S3 with minimal manual intervention.
- **Common Task:** One-time large data migration or periodic sync between on-prem NFS and S3
- **Pricing:** $0.0125 per GB transferred

**Use Case Example:**
- Migrating 500TB of legacy data from on-prem NAS to S3 Data Lake
- Ongoing incremental sync of daily file dumps from corporate file servers

---

## [Amazon EventBridge](https://aws.amazon.com/eventbridge/)

Serverless event bus for building event-driven architectures.

- **Why it matters:** Decouple your data pipeline components with event-driven triggers beyond just S3 events.
- **Common Task:** Triggering workflows when SaaS applications emit events (Zendesk ticket created, Stripe payment received)
- **Pricing:** $1 per million events published

### Code Example - EventBridge Rule

```python
import boto3
import json

events = boto3.client('events')

# Create rule to trigger on custom event
response = events.put_rule(
    Name='new-customer-signup',
    EventPattern=json.dumps({
        "source": ["custom.app"],
        "detail-type": ["Customer Signup"]
    }),
    State='ENABLED'
)

# Add Lambda target
events.put_targets(
    Rule='new-customer-signup',
    Targets=[{
        'Id': '1',
        'Arn': 'arn:aws:lambda:us-east-1:123456789:function:process-signup'
    }]
)
```

---

## [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)

Manage, retrieve, and rotate database credentials, API keys, and other secrets.

- **Why it matters:** Never hardcode database passwords or API keys in your Glue/Lambda code again.
- **Common Task:** Storing RDS passwords, API tokens for third-party services
- **Pricing:** $0.40 per secret per month + $0.05 per 10,000 API calls

### ✅ When to Use (Security Best Practices)

1. **Database Credentials Rotation**
   - **Requirement:** Rotate DB passwords every 90 days (Compliance)
   - **Old Way:** Update app config, redeploy app, update DB user (Process takes hours)
   - **Secrets Manager:** Automatic rotation with Lambda (Zero downtime)
   - **Value:** Eliminates hardcoded credentials and manual rotation toil

2. **Sharing Secrets Across Environments**
   - **Scenario:** Dev, Test, Prod environments need different API keys
   - **Implementation:** Inject secrets as env variables at runtime
   - **Security:** Developers never see Prod keys; only the app does
   - **Cost:** ~$0.40/month per key is negligible for security gain

3. **Cross-Account Access**
   - **Use Case:** Centralized EMR cluster accessing RDS in another account
   - **Solution:** Resource-based policies on the Secret
   - **Alternative:** Hardcoding credentials in scripts (High security risk)

### ❌ When NOT to Use

- **High-volume reads without caching:** Calling `GetSecretValue` inside a loop 1000x/sec will get expensive ($0.05/10k calls). Always cache secrets in your application memory.
- **Non-sensitive config:** Use Systems Manager Parameter Store (Standard) for plain text config strings (it's free). Use Secrets Manager only for actual secrets (passwords, keys).

### Code Example - Retrieve Secret in Lambda

```python
import boto3
import json

def lambda_handler(event, context):
    secrets_client = boto3.client('secretsmanager')
    
    # Get database password
    response = secrets_client.get_secret_value(SecretId='prod/db/password')
    secret = json.loads(response['SecretString'])
    
    db_password = secret['password']
    db_username = secret['username']
    
    # Use credentials to connect to database
    # ...
```

### Best Practices

- Enable **automatic rotation** for database credentials (30-90 days)
- Use **IAM policies** to restrict who can read specific secrets
- Reference secrets in Glue jobs using connection properties

---

## [Amazon QuickSight](https://aws.amazon.com/quicksight/)

Cloud-native Business Intelligence (BI) service for building dashboards and visual analytics.

- **Why it matters:** Native AWS BI tool with ML-powered insights, cheaper than Tableau/PowerBI for large teams.
- **Common Task:** Building executive dashboards on top of Redshift or Athena data
- **Pricing:** $9-18/user/month (Standard) or $24/user/month (Enterprise)

**Integration Points:**
- Direct connector to **Athena** (query S3 data lakes)
- Direct connector to **Redshift**
- Can use **SPICE** (in-memory engine) for faster dashboards
- Supports embedded analytics in web applications

---

## [AWS Transfer Family](https://aws.amazon.com/aws-transfer-family/)

Fully managed SFTP, FTPS, and FTP service directly into S3.

- **Why it matters:** Legacy systems and partners often require SFTP. This eliminates the need for EC2-based SFTP servers.
- **Common Task:** Receiving daily data files from external vendors via SFTP, landing directly in S3
- **Pricing:** ~$0.30/hour + $0.04 per GB transferred

---

## [Amazon Timestream](https://aws.amazon.com/timestream/)

Fast, scalable, serverless time-series database.

- **Why it matters:** Optimized for IoT, DevOps monitoring, and real-time analytics on time-stamped data.
- **Common Task:** Storing and querying IoT sensor data, metrics, and logs at scale
- **Pricing:** $0.50 per million writes, $0.01 per GB scanned for queries

**When to Use:**
- **IoT workloads**: Millions of sensor readings per second
- **DevOps metrics**: Application performance monitoring
- **Alternative to**: DynamoDB or Redshift for time-series specific use cases

---

## Related Topics

- **[ETL & Integration](04_etl_integration.md)**: DataSync complements DMS and AppFlow
- **[Governance & Catalog](07_governance_catalog.md)**: Secrets Manager for secure credentials
- **[Daily Workflow](16_daily_workflow.md)**: When to use these niche services

[← Back to Main](../README.md)
