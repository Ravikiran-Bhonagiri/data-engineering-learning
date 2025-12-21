# Governance & Catalog 🛡️

[← Back to Main](README.md)

Secure, govern, and discover your data assets in GCP.

---

## [Data Catalog](https://cloud.google.com/data-catalog)

Fully managed metadata management and data discovery service.

- **Why it matters:** Find and understand data across your organization
- **Common Task:** Search for tables, understand schemas, track lineage
- **Pricing:** Free for GCP metadata; $10/100K API calls for custom entries

### ✅ When to Use (Data Discovery)

1. **Data Discovery (Find tables/datasets)**
   - **Search:** "customer email" finds all tables with that column
   - **Metadata:** Automatic for BigQuery, Cloud Storage, Pub/Sub
   - **User Experience:** Data analysts find data without asking IT
   - **Cost:** Free for GCP native services

2. **Data Governance (Document & Tag)**
   - **Business Context:** Add descriptions, ownership
   - **Policy Tags:** Mark PII, sensitive data
   - **Integration:** Works with DLP for automated classification
   - **When:** Team >10 people needs shared understanding

3. **Schema Understanding**
   - **Auto-discovery:** Schemas from BigQuery, Cloud Storage
   - **Documentation:** Add column descriptions
   - **Version History:** Track schema changes
   - **Value:** New team members onboard faster

### ❌ When NOT to Use

- **Small team (<5 people):** Manual documentation might be simpler
- **Single system:** If only using BigQuery, its native UI may suffice
- **No governance needs:** Overkill for simple projects

---

## [Cloud DLP (Data Loss Prevention)](https://cloud.google.com/dlp)

Discover, classify, and protect sensitive data.

- **Why it matters:** Automatically find and redact PII (SSN, credit cards, emails)
- **Common Task:** Scan BigQuery for PII, mask sensitive data
- **Pricing:** $1.25/GB inspected for unstructured data (first 1GB/month free)

### ✅ When to Use (PII Protection)

1. **PII Discovery (Find sensitive data)**
   - **Auto-detect:** SSN, credit cards, phone numbers, emails
   - **Scan:** BigQuery tables, Cloud Storage files
   - **Cost:** Scan 100GB = $125 (one-time scan)
   - **Value:** Compliance (GDPR, HIPAA, PCI)

2. **Data Masking (Redact before analysis)**
   - **Techniques:** Redaction, masking, tokenization
   - **Example:** Replace SSN with XXX-XX-1234
   - **Use Case:** Share data with analysts without exposing PII
   - **Integration:** Works with Data Catalog tags

3. **Compliance Automation**
   - **Continuous Scanning:** Alert when PII found
   - **Policy Enforcement:** Block BigQuery exports with PII
   - **Audit Logs:** Track who accessed sensitive data
   - **When:** Regulatory requirements (SOC2, HIPAA)

### ❌ When NOT to Use

- **No sensitive data:** Public datasets don't need DLP
- **Cost-sensitive:** $1.25/GB expensive for frequent scans; scan once, tag with Data Catalog, then use tags
- **Simple use cases:** Manual review cheaper for small datasets (<10GB)

---

## [IAM (Identity and Access Management)](https://cloud.google.com/iam)

Control who can access what in GCP.

- **Why it matters:** Foundational security for all GCP services
- **Common Task:** Grant data engineers access to BigQuery, deny access to PII tables
- **Pricing:** Free

### ✅ When to Use (Always - Security Foundation)

1. **Principle of Least Privilege**
   - **Grant Minimum:** Only what's needed for the job
   - **Example:** Analysts get BigQuery read-only, not write
   - **Service Accounts:** For Dataflow, Cloud Composer automation
   - **Cost:** Free, but critical for security

2. **Role-Based Access Control (RBAC)**
   - **Predefined Roles:** BigQuery Data Viewer, Data Editor, Admin
   - **Custom Roles:** Create specific permissions
   - **Example:** "Can query non-PII tables only"
   - **Scale:** Manage 100+ users with groups

3. **Resource Hierarchy**
   - **Organization → Folders → Projects → Resources**
   - **Inheritance:** Permissions flow down
   - **Example:** Grant all data engineers access to "Analytics" folder
   - **When:** Multi-team, multi-project organization

### Best Practices

- **Use service accounts** for applications (not user accounts)
- **Enable 2FA/MFA** for all users
- **Audit with Cloud Logging** - track all access
- **Regular access reviews** - remove unused permissions
- **Separate dev/prod** - different projects with different permissions

---

## Integration: Catalog + DLP + IAM

**Powerful Combo:**
1. **DLP scans** BigQuery, finds PII
2. **Data Catalog** gets policy tags applied automatically
3. **IAM policies** enforce who can see PII-tagged columns
4. **Result:** Automatic PII protection across organization

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: Column-level security with policy tags
- **[Monitoring](09_monitoring_logging.md)**: Audit logs for access tracking
- **[Daily Workflow](13_daily_workflow.md)**: Governance in pipeline design

[← Back to Main](README.md)
