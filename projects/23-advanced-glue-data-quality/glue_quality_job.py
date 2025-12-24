import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# 1. Initialize Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 2. Source Data (Simulated)
# In real life: glueContext.create_dynamic_frame.from_catalog(...)
print("Reading Source Data...")
df_input = spark.createDataFrame([
    (1, "alice@example.com", 25),
    (2, "bob@example.com", -5),   # BAD: Negative Age
    (3, None, 30)                 # BAD: Null Email
], ["id", "email", "age"])

dyf_input = glueContext.create_dynamic_frame.fromDF(df_input, glueContext, "dyf_input")

# 3. Define Data Quality Rules (DQDL)
# This is the dedicated language for Glue DQ
dqdl_rules = """
Rules = [
    IsComplete "email",
    ColumnValues "age" > 0,
    IsUnique "id"
]
"""

print(f"Applying Data Quality Rules:\n{dqdl_rules}")

# 4. Evaluate Data Quality
# This transform runs the checks against the DynamicFrame
dq_results = EvaluateDataQuality().process_rows(
    frame=dyf_input,
    ruleset=dqdl_rules,
    publishing_options={
        "dataQualityEvaluationContext": "eval_context_1",
        "enableDataQualityCloudWatchMetrics": True,
        "enableDataQualityResultsPublishing": True
    },
    additional_options={"performanceTuning.caching": "CACHE_NOTHING"}
)

# 5. Handle Results (The Circuit Breaker)
# dq_results contains the row-level outcomes & overall score.
# We check if the job should fail.

# (Simulation logic as EvaluateDataQuality is hard to run locally without AWS libs)
print("--- Quality Evaluation Completed ---")
print("Row 2 Failed: ColumnValues 'age' > 0 (Actual: -5)")
print("Row 3 Failed: IsComplete 'email' (Actual: NULL)")

# 6. Filtering (Optional)
# In a real job, you might split the stream:
# Good Data -> Write to S3
# Bad Data -> Write to Quarantine Bucket

print("Writing 'Good' data to S3 (Filtered)...")
# glueContext.write_dynamic_frame...

job.commit()
