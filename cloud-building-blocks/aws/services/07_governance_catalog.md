# Governance & Catalog 🛡️

[← Back to Main](../README.md)

Data is only valuable if you can find it and secure it.

---

## [AWS Glue Data Catalog](https://aws.amazon.com/glue/features/#Data_Catalog)

A central repository to store structural and operational metadata for all your data assets.

- **Why it matters:** It's the "Map" of your data lake. Services like Athena and Redshift Spectrum use it to know where files are and what columns they have.
- **Common Task:** Registering tables so Athena can query them
- **Pricing:** First million objects stored free, then $1 per 100,000 objects/month

### ✅ When to Use (Security & Governance at Scale)

1. **Column-Level Security (PII Protection)**
   - **Requirement:** Hide `ssn` and `dob` columns from Data Analysts
   - **Old Way:** Duplicate data into "secure" buckets/tables (storage x2)
   - **Lake Formation:** Define policy once, applied dynamically at query time
   - **Value:** Zero data duplication, centralized audit

2. **Cross-Account Data Sharing (No Copying)**
   - **Scenario:** Marketing account needs sales data from Finance account
   - **Start Simple:** S3 Bucket Policies (messy, hard to audit)
   - **Lake Formation:** "Grant Select" to external account ID
   - **Efficiency:** No ETL required; data stays in place

3. **Fine-Grained Access Control (Row-level)**
   - **Use Case:** Regional managers see only their region's sales
   - **Implementation:** Data filters (WHERE region='US-East')
   - **Alternative:** Create 50 views for 50 regions (maintenance nightmare)
   - **Complexity:** High initial setup, low long-term maintenance

4. **Centralized Permissions Management**
   - **Problem:** Managing IAM policies for 100 users across S3/Glue/Athena
   - **Solution:** Manage permissions in one dashboard (Lake Formation)
   - **Audit:** "Who has access to the Sales table?" -> Single report
   - **When:** Team grows >5 people or compliance audit is required

### ❌ When NOT to Use

- **Small/Single-Team Projects:** IAM roles and S3 bucket policies are simpler and faster to setup
- **Non-Glue/Athena Access:** If accessing S3 directly via custom apps (boto3), Lake Formation permissions don't always apply (unless using specific patterns)
- **Over-governance early on:** Don't implement column-level security for public datasets; adds unnecessary friction

### Best Practices

- Use **Glue Crawlers** to auto-populate the catalog
- Version your schema definitions
- Add **table properties** for documentation and lineage

---

## [AWS Lake Formation](https://aws.amazon.com/lake-formation/)

A service that makes it easy to set up a secure data lake in days.

- **Why it matters:** It provides fine-grained access control (column-level and row-level security) across your S3 files.
- **Common Task:** Granting read-only access to specific tables/columns for analysts

---

## [AWS IAM (Identity and Access Management)](https://aws.amazon.com/iam/)

Manage access to AWS services and resources securely.

- **Why it matters:** Foundational security. Every AWS service interaction requires IAM permissions.
- **Common Task:** Creating role-based policies for data engineers, analysts, and automated jobs

### Best Practices

- Follow **principle of least privilege**
- Use **IAM Roles** for EC2, Lambda, Glue (not hardcoded credentials)
- Enable **MFA** for administrative users
- Use **Service Control Policies (SCPs)** for organization-level governance

---

## Related Topics

- **[Advanced Architectures](15_advanced_architectures.md)**: Data lake security patterns
- **[Advanced Services](10_advanced_services.md)**: Secrets Manager for credential management
- **[Monitoring & Logging](09_monitoring_logging.md)**: CloudTrail for audit logs

[← Back to Main](../README.md)
