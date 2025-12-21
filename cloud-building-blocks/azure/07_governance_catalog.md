# Governance & Catalog 🛡️

[← Back to Main](README.md)

Discover, classify, and govern your data estate.

---

## [Microsoft Purview](https://azure.microsoft.com/services/purview/)

Unified data governance service.

- **Why it matters:** Data discovery, lineage, classification across Azure/on-prem/multi-cloud
- **Pricing:** ~$0.40/vCore-hour + $1.20/GB scanned (one-time)

### ✅ When to Use

1. **Data Discovery**
   - **Search:** Find tables/columns across entire data estate
   - **Metadata:** Automatic from Azure sources
   - **When:** Team >10 people, multi-source

2. **Data Lineage**
   - **Track:** Data from source → transformations → destination  
   - **Integration:** Data Factory, Synapse, Databricks
   - **When:** Compliance, impact analysis

3. **Sensitive Data Classification**
   - **Auto-scan:** Find PII, financial data
   - **Cost:** $1.20/GB scanned (one-time)
   - **When:** GDPR, HIPAA compliance

### ❌ When NOT to Use

- **Small team (<5):** Manual documentation simpler
- **Single source:** Native tools may suffice

---

## [Azure Policy](https://azure.microsoft.com/services/azure-policy/)

Enforce organizational standards and compliance at scale.

- **Pricing:** Free

### ✅ When to Use (Always - Governance)

- **Compliance:** Enforce tagging, naming, regions
- **Cost control:** Prevent expensive resources
- **Security:** Block public access, require encryption

[← Back to Main](README.md)
