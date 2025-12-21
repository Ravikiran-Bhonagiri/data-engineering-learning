# Installation Guide

**Detailed setup for all environments.**

---

## Option 1: pip (Local Development)

### Prerequisites
- Python 3.8+ 
- Java 8 or 11p (required by Spark)

### Step 1: Install Java

**Windows:**
```powershell
# Download from https://adoptium.net/
# After install, set JAVA_HOME:
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-11", "User")
$env:Path += ";$env:JAVA_HOME\bin"
```

**Mac:**
```bash
brew install openjdk@11
echo 'export JAVA_HOME=/usr/local/opt/openjdk@11' >> ~/.zshrc
source ~/.zshrc
```

**Linux:**
```bash
sudo apt update
sudo apt install openjdk-11-jdk
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Create Virtual Environment

```bash
python -m venv pyspark_env
source pyspark_env/bin/activate  # Windows: pyspark_env\Scripts\activate
```

### Step 3: Install PySpark

```bash
pip install pyspark
```

### Step 4: Verify

```bash
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.getOrCreate(); print(spark.version)"
```

---

## Option 2: Conda

```bash
# Create environment
conda create -n pyspark python=3.10 -y
conda activate pyspark

# Install PySpark
conda install -c conda-forge pyspark -y

# Optional: Jupyter
conda install jupyter -y
```

---

## Option 3: Docker (No Java Setup!)

### Quick Start

```bash
# Pull image
docker pull jupyter/pyspark-notebook

# Run with port mapping
docker run -it --rm \
    -p 8888:8888 \
    -p 4040:4040 \
    -v $(pwd):/home/jovyan/work \
    jupyter/pyspark-notebook
```

### Custom Dockerfile

```dockerfile
FROM apache/spark-py:v3.5.0

USER root
RUN pip install pandas numpy delta-spark
USER spark

WORKDIR /app
COPY . .

CMD ["spark-submit", "main.py"]
```

---

## Option 4: Databricks (Cloud)

1. Create account at [databricks.com](https://databricks.com)
2. Launch workspace
3. Create cluster
4. Open notebook - Spark is pre-configured!

```python
# Databricks notebooks have spark pre-initialized
display(spark.range(10))
```

---

## Option 5: Google Colab (Free)

```python
# Install PySpark in Colab
!pip install pyspark

# Use it
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
```

---

## 🔧 Troubleshooting Installation

### Error: "JAVA_HOME not set"

```bash
# Check if Java is installed
java -version

# Set JAVA_HOME (Linux/Mac)
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
```

### Error: "Python version mismatch"

```bash
# Use specific Python version
pyspark --python python3.10
```

### Error: "Port 4040 already in use"

```python
spark = SparkSession.builder \
    .config("spark.ui.port", 4041) \
    .getOrCreate()
```

---

## 📦 Common Packages

```bash
# Core
pip install pyspark

# Delta Lake
pip install delta-spark

# ML extras
pip install pyspark[ml]

# All extras
pip install pyspark[sql,ml,streaming]
```

---

**You're ready to start learning!** 🚀
