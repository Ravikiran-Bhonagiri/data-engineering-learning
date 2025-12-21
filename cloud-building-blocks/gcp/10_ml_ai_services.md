# ML & AI Services 🤖

[← Back to Main](README.md)

Machine learning and AI capabilities for data engineering workflows.

---

## [Vertex AI](https://cloud.google.com/vertex-ai)

Unified ML platform for training, deploying, and managing models.

- **Why it matters:** End-to-end ML without managing infrastructure
- **Common Task:** Train models on BigQuery data, deploy predictions
- **Pricing:** Varies by compute (e.g., $0.49/hour for n1-standard-4 training)

### ✅ When to Use (ML Platform)

1. **BigQuery ML Alternative (More features)**
   - **BigQuery ML:** SQL-only, limited algorithms
   - **Vertex AI:** Full Python, any framework (TensorFlow, PyTorch, scikit-learn)
   - **When:** BigQuery ML too limiting
   - **Cost:** Training job on n1-standard-4 = $0.49/hr

2. **AutoML (No-Code ML)**
   - **Users:** Non-ML experts
   - **Types:** AutoML Tables, Vision, NLP
   - **Example:** Predict customer churn with CSV upload
   - **Cost:** ~$19.32/hour for training
   - **When:** No data scientists on team

3. **Model Pipeline Orchestration**
   - **Vertex Pipelines:** Kubeflow-based
   - **Workflow:** Data prep → Train → Evaluate → Deploy
   - **Integration:** Works with BigQuery, Cloud Storage
   - **When:** Production ML pipelines

4. **Model Deployment & Monitoring**
   - **Endpoints:** Serve predictions via API
   - **Autoscaling:** Handle variable traffic
   - **Monitoring:** Track model drift
   - **Cost:** $0.056/hour per node (n1-standard-2)

### ❌ When NOT to Use

- **Simple analytics:** BigQuery SQL or BigQuery ML sufficient
- **No ML expertise:** Start with BigQuery ML before Vertex AI
- **Cost-constrained:** Training can be expensive; use BigQuery ML first
- **One-off analysis:** Colab notebooks might be simpler

---

## [BigQuery ML](https://cloud.google.com/bigquery-ml)

Create and execute machine learning models using SQL.

- **Why it matters:** ML without leaving BigQuery (no Python needed)
- **Common Task:** Predict customer lifetime value directly in SQL
- **Pricing:** Included in BigQuery pricing (query costs apply)

### ✅ When to Use (SQL-Based ML)

1. **Start Simple (No Python/frameworks)**
   - **Algorithms:** Linear regression, logistic regression, clustering, time series
   - **Syntax:** CREATE MODEL with SQL
   - **No Data Movement:** Train on data already in BigQuery
   - **Cost:** Pay only for BigQuery query processing

2. **Quick Prototyping**
   - **Speed:** Build model in hours vs days
   - **Iteration:** SQL queries vs Python notebooks
   - **Example:** Predict churn for proof-of-concept
   - **Graduate:** Move to Vertex AI if needs grow

3. **Data-Centric ML (Features in BigQuery)**
   - **Feature Store:** BigQuery tables
   - **No ETL:** Data already transformed in BigQuery
   - **Integration:** Predictions written back to BigQuery
   - **When:** All your data lives in BigQuery

### Code Example - BigQuery ML

```sql
-- Train model
CREATE OR REPLACE MODEL `dataset.customer_churn_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['churned']
) AS
SELECT 
  age,
  total_spend,
  months_active,
  churned
FROM `dataset.customers`
WHERE date < '2024-01-01';

-- Make predictions
SELECT 
  customer_id,
  predicted_churned,
  predicted_churned_probs[OFFSET(1)].prob as churn_probability
FROM ML.PREDICT(MODEL `dataset.customer_churn_model`,
  (SELECT * FROM `dataset.new_customers`));
```

### ❌ When NOT to Use

- **Need deep learning:** BigQuery ML doesn't support custom neural nets
- **Complex feature engineering:** Use Dataflow or Vertex AI
- **Model needs to run outside BigQuery:** Use Vertex AI for portable models

---

## Decision: BigQuery ML vs Vertex AI

| Factor | BigQuery ML | Vertex AI |
|--------|-------------|-----------|
| **Skill Level** | SQL only | Python/ML expertise |
| **Algorithms** | 10+ basic algorithms | Any framework |
| **Cost** | BigQuery query costs | Compute + storage |
| **Use Case** | Quick models, prototypes | Production ML |
| **Deployment** | BigQuery predictions | API endpoints |
| **When** | Start here | Graduate when needed |

**Recommendation:** Start with BigQuery ML → Move to Vertex AI when you need:
- Custom models
- Non-tabular data (images, text)
- Model serving outside BigQuery
- Advanced model monitoring

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: BigQuery ML native integration
- **[Dataflow](02_compute_processing.md)**: Feature engineering pipelines
- **[Service Comparisons](11_service_comparisons.md)**: BigQuery ML vs Vertex AI

[← Back to Main](README.md)
