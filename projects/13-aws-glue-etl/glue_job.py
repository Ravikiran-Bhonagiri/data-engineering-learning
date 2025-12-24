import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# 1. Boilerplate Setup
# Glue jobs require specific arguments (like JOB_NAME)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 2. Source (DynamicFrame)
# Instead of spark.read.parquet, we use create_dynamic_frame.from_catalog
print("Reading from Glue Catalog...")
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "finance_db", 
    table_name = "raw_customers", 
    transformation_ctx = "datasource0"
)

# 3. Transform (ApplyMapping)
# This is valid JSON that maps [SourceCol, SourceType] -> [TargetCol, TargetType]
print("Applying Mapping...")
applymapping1 = ApplyMapping.apply(
    frame = datasource0, 
    mappings = [
        ("customer_id", "string", "id", "long"),       # Rename & Cast
        ("full_name", "string", "name", "string"),     # Rename
        ("signup_ts", "string", "created_at", "timestamp") # Cast
    ], 
    transformation_ctx = "applymapping1"
)

# 4. Conversion (Optional)
# You can convert to standard Spark DataFrame if you need complex logic
df = applymapping1.toDF()
df_filtered = df.filter("id IS NOT NULL")

# Convert back to DynamicFrame for writing
dynamic_frame_write = DynamicFrame.fromDF(df_filtered, glueContext, "dynamic_frame_write")

# 5. Sink (S3 Parquet)
print("Writing to S3...")
datasink2 = glueContext.write_dynamic_frame.from_options(
    frame = dynamic_frame_write, 
    connection_type = "s3", 
    connection_options = {"path": "s3://my-datalake-bucket/clean-customers/"}, 
    format = "parquet", 
    transformation_ctx = "datasink2"
)

job.commit()
print("Job Committed.")
