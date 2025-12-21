# Extracted from pyspark-plan.pdf

# **7‑Day Comprehensive Plan to Learn PySpark**



This 7‑day plan with Day 0 is designed for data engineers or analysts who know Python and want to master
PySpark. PySpark is the **Python API for Apache Spark**, allowing you to perform **real‑time, large‑scale data**
**processing in a distributed environment** [1](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) . It combines Python’s ease of use with Spark’s power,
enabling data processing and analysis at any size [2](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) . PySpark supports modules such as **Spark SQL**,
**DataFrames**, **Structured Streaming**, **MLlib**, and **Spark Core** [3](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20supports%20all%20of%20Spark%E2%80%99s,Pipelines%20and%20Spark%20Core) . Before PySpark, processing big data in
Python often meant using Pandas on a single machine or resorting to complex Hadoop MapReduce jobs;
these approaches struggled with scalability and required low‑level Java or Scala coding. PySpark addresses
these problems by offering a high‑level, distributed computing framework accessible to Python developers

[4](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20is%20a%20Python%20Apache,Here%20is%20the%20official%20documentation) .



[1](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data)



[2](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data)



[3](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20supports%20all%20of%20Spark%E2%80%99s,Pipelines%20and%20Spark%20Core)



[4](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20is%20a%20Python%20Apache,Here%20is%20the%20official%20documentation)


## **Day 0 – What Is PySpark and Why It Matters**

**Goals:** Understand the PySpark ecosystem, why it’s needed, and how it differs from traditional Python data
processing. Explore an example that illustrates the difference between a single‑node Pandas workflow and
a distributed PySpark workflow.


**🔍 Before PySpark: Single‑Node Python vs Distributed Spark**


Traditional Python tools like **Pandas** excel on small to medium datasets but struggle when data no longer
fits in memory. Python scripts running on one machine cannot distribute work across a cluster, leading to
slow processing and memory bottlenecks. Earlier big‑data solutions used **MapReduce**, which required
writing verbose Java/Scala code and lacked an interactive API.


**How PySpark Solves These Problems**



PySpark exposes the power of Apache Spark to Python programmers [2](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) . It processes data **in memory**,
which is faster than disk‑based systems [5](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20excels%20in%20large,a%20simple%20interface%20in%20a), and can scale from **one workstation to thousands of nodes**

[6](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=From%20one%20workstation%20to%20thousands,Streaming%20to%20detect%20banking%20fraud) . PySpark’s ecosystem includes: - **Spark SQL and DataFrames** for working with structured data using

SQL or DataFrame APIs [7](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20SQL%20and%20DataFrames) . - **Structured Streaming** for scalable, fault‑tolerant stream processing [8](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Structured%20Streaming) . **MLlib** for machine learning pipelines and algorithms [9](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Machine%20Learning%20) . - **Spark Core and RDDs** for low‑level
transformations and fault‑tolerant operations [10](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20Core%20and%20RDDs) .



[2](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data)



[5](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20excels%20in%20large,a%20simple%20interface%20in%20a)



[6](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=From%20one%20workstation%20to%20thousands,Streaming%20to%20detect%20banking%20fraud)



[7](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20SQL%20and%20DataFrames) [8](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Structured%20Streaming)



[9](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Machine%20Learning%20)



[10](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20Core%20and%20RDDs)



These components enable you to build complex ETL, analytics and machine learning pipelines entirely in
Python. PySpark’s in‑memory execution and distributed architecture handle big data efficiently [11](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20excels%20in%20large,interface%20in%20a%20complicated%20system) .


**Example: Pandas vs PySpark**


Suppose you need to analyze terabytes of web‑log data to compute daily user metrics. Using Pandas on a
laptop would quickly exhaust memory. With PySpark, you can:


1


```
 from pyspark.sql import SparkSession

 spark = SparkSession.builder.appName("web_log_metrics").getOrCreate()

 # Read logs from a distributed storage (e.g., HDFS or S3)
 logs = spark.read.json("s3://logs/2025/")

 # Compute daily unique users and page views
 import pyspark.sql.functions as F
 metrics = logs.groupBy("date").agg(
   F.countDistinct("user_id").alias("unique_users"),
   F.count("url").alias("page_views")
 )

 metrics.show()

```

This distributed DataFrame computation runs across many nodes, handles terabytes of data, and leverages
Spark’s Catalyst optimizer for performance [12](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=2.%20SQL,mechanisms%20like%20Tungsten%20for%20physical) .

## **Day 1 – Installation and First Steps**


**Objectives:** Install PySpark locally (or use Databricks/EMR), understand the Spark architecture (driver,
executors, cluster manager), and create your first RDD.



1.


2.



**Install PySpark** using pip or Conda. If you’re working on a cluster, ensure Java and Python are
installed and configure environment variables.
**Start a Spark session** in a Python script or interactive shell:


```
from pyspark.sql import SparkSession
spark =
SparkSession.builder.master("local[*]").appName("learn_pyspark").getOrCreate()

```


1.


2.



**Understand Spark components** : The **driver** coordinates tasks; **executors** run tasks; a **cluster**
**manager** (e.g., YARN, Kubernetes) allocates resources.
**Create your first RDD** (Resilient Distributed Dataset) by parallelizing a Python list or reading a text
file:


```
 data = [("apple", 1), ("banana", 2), ("orange", 3)]
 rdd = spark.sparkContext.parallelize(data)

```

5. **Perform simple transformations and actions** on the RDD (e.g., `map`, `filter`, `collect` ) to get

comfortable with the low‑level API. Remember that RDDs offer fine‑grained control and fault tolerance [13](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=1.%20Low,in%20processing%20diverse%20data%20types) .


2


**Deliverables:** A working PySpark installation; a script that initializes a Spark session, creates an RDD,
performs a transformation and prints results.

## **Day 2 – Mastering RDDs**


**Objectives:** Learn RDD transformations and actions, understand fault tolerance and immutability, and
recognize RDD limitations.



1.


2.


3.


4.


5.



**Explore transformations** : Use `map`, `flatMap`, `filter`, `reduceByKey`, and `join` to

transform data. RDD operations are **lazy** —they only execute when an action (e.g., `collect`,

`count`, `saveAsTextFile` ) triggers computation.

**Understand RDD benefits** : RDDs provide **fine‑grained control**, fault tolerance through lineage,



immutability and flexibility to handle unstructured data [13](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=1.%20Low,in%20processing%20diverse%20data%20types) .
**Recognize RDD limitations** : RDDs lack built‑in optimizations, requiring you to manually optimize
code for performance [14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD) . The API is more complex and lacks schema enforcement [14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD), making it
harder to debug and integrate with SQL.
**Practice** : Write an RDD program that counts the number of occurrences of each word in a large text
file. Introduce a fault (e.g., kill an executor) and observe how Spark recovers due to fault tolerance.
**Notes** : Although RDDs are foundational, Spark’s documentation recommends using DataFrames and
SQL for most workloads because they provide optimization and a simpler API [10](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20Core%20and%20RDDs) .



[13](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=1.%20Low,in%20processing%20diverse%20data%20types)



[14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD) [14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD)



[10](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20Core%20and%20RDDs)



**Deliverables:** A script that processes text using RDDs and demonstrates fault tolerance; a summary of
when to prefer RDDs vs DataFrames.

## **Day 3 – DataFrames and Spark SQL**


**Objectives:** Learn to create and manipulate DataFrames, understand the Catalyst optimizer, and mix SQL
with Python.



1.



[15](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=It%20was%20introduced%20first%20in,not%20allowed%20with%20the%20RDDs)



2. **Advantages of DataFrames** :
3. Built‑in optimization via the **Catalyst optimizer**, which automatically optimizes query plans [16](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=3,friendly%20API%20than%20RDDs%2C%20with)



4. Rich API for filtering, aggregation and joins [17](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=for%20filtering%2C%20aggregation%2C%20joining%2C%20and,better%20join%20strategies)



5. Schema enforcement and compatibility with BI tools [18](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=%28e,mechanisms%20like%20Tungsten%20for%20physical)



6. Optimized storage formats (Parquet, ORC) and integration with Hive, JDBC, S3.
7. Faster performance and lower memory consumption than RDDs [19](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=6,mechanisms%20like%20Tungsten%20for%20physical)



8.



**Create DataFrames** from lists, dictionaries, CSV, JSON, or Parquet files. DataFrames are distributed
collections of data organized into named columns [15](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=It%20was%20introduced%20first%20in,not%20allowed%20with%20the%20RDDs) .
**Advantages of DataFrames** :
Built‑in optimization via the **Catalyst optimizer**, which automatically optimizes query plans [16](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=3,friendly%20API%20than%20RDDs%2C%20with) .
Rich API for filtering, aggregation and joins [17](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=for%20filtering%2C%20aggregation%2C%20joining%2C%20and,better%20join%20strategies) .
Schema enforcement and compatibility with BI tools [18](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=%28e,mechanisms%20like%20Tungsten%20for%20physical) .
Optimized storage formats (Parquet, ORC) and integration with Hive, JDBC, S3.
Faster performance and lower memory consumption than RDDs [19](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=6,mechanisms%20like%20Tungsten%20for%20physical) .
**Use Spark SQL** : Register a DataFrame as a temporary view and run SQL queries:


```
df = spark.read.csv("data/transactions.csv", header=True, inferSchema=True)
df.createOrReplaceTempView("transactions")
result = spark.sql("SELECT customer_id, SUM(amount) AS total_spent FROM

```

3


```
 transactions GROUP BY customer_id")
 result.show()

```

4. **Practice** : - Load a CSV into a DataFrame; print schema; filter rows; group by categories; compute
aggregates. - Join two DataFrames (e.g., customers and orders) and perform calculations. - Use built‑in
functions (e.g., `withColumn`, `when` ) for feature engineering. 5. **Discuss DataFrame limitations** :

DataFrames lack compile‑time type safety and may not catch certain errors until runtime [14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD) . However, they
strike a balance between flexibility and performance.


**Deliverables:** A notebook demonstrating DataFrame creation, querying with SQL, and joining tables; notes
comparing DataFrames and RDDs.

## **Day 4 – Structured Streaming**


**Objectives:** Understand Spark’s structured streaming engine and build your first streaming application.



1.


2.



**Learn about structured streaming** : It treats streaming data as an unbounded table, allowing you
to write queries with the same API used for batch processing [20](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Structured%20Streaming) .
**Set up a streaming source** : Use a socket or directory source to ingest streaming data. For example:


```
from pyspark.sql.functions import explode, split

# Read lines of text from a socket
lines = spark.readStream.format("socket").option("host",
"localhost").option("port", 9999).load()
words = lines.select(explode(split(lines.value, " ")).alias("word"))
wordCounts = words.groupBy("word").count()

query = wordCounts.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()

```


1.


2.


3.



**Understand triggers and checkpoints** : Use `writeStream` options to set output modes (append,

complete), triggers (processing time), and checkpoint locations for fault tolerance.
**Practice** : Build a streaming pipeline that ingests JSON events (e.g., user clicks), performs
aggregations (e.g., counts per page), and writes results to a sink (console or file). Consider time
windows and watermarking to handle late data.
**Discuss limitations** : Structured streaming processes data in micro‑batches; it is not as low‑latency
as dedicated streaming engines. However, it provides fault tolerance and unified batch/stream APIs.



**Deliverables:** A streaming application that counts words or events in real time; notes on triggers,
checkpoints, and output modes.


4


## **Day 5 – Machine Learning and Graph Analytics**

**Objectives:** Explore Spark’s machine learning library (MLlib) and graph processing capabilities.



1.


2.
3.
4.

5.
6.
7.
8.

9.


10.


11.



**Introduction to MLlib** : MLlib provides scalable algorithms for classification, regression, clustering
and recommendation. It integrates tightly with DataFrames and Spark’s pipeline API [9](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Machine%20Learning%20) .
**Build a machine learning pipeline** :
Load and prepare data using DataFrames.
Assemble features with `VectorAssembler` .

Split data into training and test sets.
Train a model (e.g., logistic regression or random forest).
Evaluate the model with metrics (accuracy, ROC).
Use `Pipeline` to chain transformers and estimators.

**Explore GraphX/GraphFrames** (if available) for graph analytics. Create vertices and edges
DataFrames and perform PageRank or connected components.
**Practice** : Implement a classification task using the Titanic or credit card fraud dataset. Use
cross‑validation and grid search for hyperparameter tuning.
**Discuss limitations** : Some MLlib algorithms may lag behind scikit‑learn features, and support for
advanced deep learning requires external libraries. GraphX is not fully available in PySpark;
GraphFrames offers limited functionality.



**Deliverables:** A notebook with a complete machine learning pipeline; optional graph analysis example.

## **Day 6 – Performance Tuning and User‑Defined Functions (UDFs)**


**Objectives:** Learn to optimize PySpark jobs, use caching and partitioning, and understand the trade‑offs of
Python UDFs.



1.


2.


3.

4.


5.
6.
7.
8.

9.



**Caching and persistence** : Use `cache()` or `persist()` to keep intermediate results in memory.

Persist only when necessary to avoid memory pressure.

**Partitioning** : Repartition or coalesce DataFrames to control the number of partitions. Understand
shuffle operations and how they affect performance.
**Broadcast joins** : For small lookup tables, use `broadcast()` to avoid shuffling.

**Avoid Python UDFs when possible** : PySpark runs Python code in separate worker processes,
causing overhead due to **serialization between Python and JVM** [21](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=PySpark%20provides%20a%20Python%20wrapper,serialization%20between%20Python%20and%20JVM) . UDFs introduce high latency
and memory usage [22](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=Why%20PySpark%20Consumes%20More%20Memory%3F) and make Spark unable to optimize execution. Prefer built‑in functions



**Performance tuning** :
Use the Spark UI to identify stages, tasks and bottlenecks.
Adjust configuration settings (e.g., executor memory, cores, shuffle partitions).
Use `explain()` to view query plans.

**Practice** : Compare the performance of a built‑in function versus an equivalent Python UDF on a
large DataFrame. Use caching and broadcast joins to optimize a join query. Adjust partition numbers
and observe changes in execution time.


5



[21](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=PySpark%20provides%20a%20Python%20wrapper,serialization%20between%20Python%20and%20JVM)




**Deliverables:** A report summarizing performance tuning experiments; code demonstrating the impact of
UDF vs built‑in functions and partitioning strategies.

## **Day 7 – Advanced Features and Integration**


**Objectives:** Explore advanced PySpark capabilities, integrate with other tools, and plan next steps.



1.


2.


3.


4.


5.



**Pandas API on Spark** : The Pandas API on Spark allows you to run pandas‑like code on distributed
data [23](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Pandas%20API%20on%20Spark) . It helps migrate existing pandas workflows to Spark with minimal changes.
**Interoperability with Python libraries** : While PySpark integrates with Pandas and NumPy,
conversions (e.g., `toPandas()` ) can be slow for large datasets [24](https://www.theknowledgeacademy.com/blog/what-is-pyspark/#:~:text=4) . Understand when to convert



and when to stay in Spark.

**Reading and writing** : Practice reading from and writing to various sources (CSV, JSON, Parquet,
JDBC, S3, Delta Lake). Use partitioned writes for large datasets.
**Cluster deployment** : Learn how to submit jobs to a cluster (e.g., via `spark-submit` ), set up

resource allocation on YARN or Kubernetes, and use Databricks or EMR for managed clusters.
**Best practices and next steps** : Review Spark’s best practices: avoid collecting large DataFrames to
the driver, minimize shuffles, use window functions judiciously. Explore Delta Lake, Structured
Streaming with event time, and advanced MLlib algorithms.



[23](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Pandas%20API%20on%20Spark)



[24](https://www.theknowledgeacademy.com/blog/what-is-pyspark/#:~:text=4)



**Deliverables:** A final project that reads real‑world data, performs transformations, trains a model, and
writes the results. Document best practices and future learning goals.


**Continuing Your Learning**



PySpark is a vast ecosystem. After completing this plan, continue practicing by: - Reading the official
PySpark documentation and user guides [25](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) . - Exploring the Pandas API on Spark for easy migration of
pandas code [23](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Pandas%20API%20on%20Spark) . - Diving deeper into structured streaming and windowed aggregations. - Learning Scala
for performance‑critical Spark applications and to access the Dataset API [21](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=PySpark%20provides%20a%20Python%20wrapper,serialization%20between%20Python%20and%20JVM) .



[25](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data)



[23](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Pandas%20API%20on%20Spark)



[21](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=PySpark%20provides%20a%20Python%20wrapper,serialization%20between%20Python%20and%20JVM)



This plan provides a structured path from fundamentals to advanced topics, combining theory with
hands‑on practice.



[1](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) [2](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data) [3](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20supports%20all%20of%20Spark%E2%80%99s,Pipelines%20and%20Spark%20Core) [7](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20SQL%20and%20DataFrames) [8](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Structured%20Streaming) [9](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Machine%20Learning%20) [10](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Spark%20Core%20and%20RDDs) [20](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Structured%20Streaming) [23](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=Pandas%20API%20on%20Spark) [25](https://spark.apache.org/docs/latest/api/python/index.html#:~:text=PySpark%20is%20the%20Python%20API,for%20interactively%20analyzing%20your%20data)



PySpark Overview — PySpark 4.1.0 documentation



[https://spark.apache.org/docs/latest/api/python/index.html](https://spark.apache.org/docs/latest/api/python/index.html)



[4](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20is%20a%20Python%20Apache,Here%20is%20the%20official%20documentation) [5](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20excels%20in%20large,a%20simple%20interface%20in%20a) [6](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=From%20one%20workstation%20to%20thousands,Streaming%20to%20detect%20banking%20fraud) [11](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/#:~:text=PySpark%20excels%20in%20large,interface%20in%20a%20complicated%20system)



What Is PySpark? Everything You Need to Know - StrataScratch



[https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/](https://www.stratascratch.com/blog/what-is-pyspark-everything-you-need-to-know/)



[12](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=2.%20SQL,mechanisms%20like%20Tungsten%20for%20physical) [13](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=1.%20Low,in%20processing%20diverse%20data%20types) [14](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=Limitations%20of%20RDD) [15](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=It%20was%20introduced%20first%20in,not%20allowed%20with%20the%20RDDs) [16](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=3,friendly%20API%20than%20RDDs%2C%20with) [17](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=for%20filtering%2C%20aggregation%2C%20joining%2C%20and,better%20join%20strategies) [18](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=%28e,mechanisms%20like%20Tungsten%20for%20physical) [19](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/#:~:text=6,mechanisms%20like%20Tungsten%20for%20physical)



RDDs vs Dataframes vs Datasets : Learn the Differences



[https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/](https://www.analyticsvidhya.com/blog/2020/11/what-is-the-difference-between-rdds-dataframes-and-datasets/)


[21](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=PySpark%20provides%20a%20Python%20wrapper,serialization%20between%20Python%20and%20JVM) [22](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a#:~:text=Why%20PySpark%20Consumes%20More%20Memory%3F) 100 Days of Data Engineering on Databricks Day 44: PySpark vs. Scala | by THE BRICK LEARNING |

Medium

[https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a](https://medium.com/@infinitylearnings1201/100-days-of-data-engineering-on-databricks-day-44-pyspark-vs-scala-c8efa539c18a)


6


[24](https://www.theknowledgeacademy.com/blog/what-is-pyspark/#:~:text=4)



What is PySpark? Features, Benefits, and Getting Started



[https://www.theknowledgeacademy.com/blog/what-is-pyspark/](https://www.theknowledgeacademy.com/blog/what-is-pyspark/)



7


