# PySpark Sample Projects

Hands-on projects to practice PySpark skills.

---

## 📁 Projects

| Project | Difficulty | Skills Practiced |
|---------|------------|------------------|
| [01_etl_pipeline.py](./01_etl_pipeline.py) | ⭐⭐ Medium | DataFrames, Transformations, Parquet |
| [02_streaming_analytics.py](./02_streaming_analytics.py) | ⭐⭐⭐ Hard | Structured Streaming, Windows |
| [03_ml_churn_prediction.py](./03_ml_churn_prediction.py) | ⭐⭐⭐ Hard | MLlib, Pipelines, CrossValidator |
| [04_data_quality_pipeline.py](./04_data_quality_pipeline.py) | ⭐⭐ Medium | Data validation, quality checks |
| [05_medallion_architecture.py](./05_medallion_architecture.py) | ⭐⭐⭐ Hard | Delta Lake, Bronze/Silver/Gold |
| [06_recommendation_engine.py](./06_recommendation_engine.py) | ⭐⭐⭐ Hard | ALS, Collaborative Filtering |

---

## 🚀 How to Run

```bash
# Local
spark-submit 01_etl_pipeline.py

# With more memory
spark-submit --driver-memory 4g --executor-memory 4g 01_etl_pipeline.py

# On cluster
spark-submit --master yarn --deploy-mode cluster 01_etl_pipeline.py
```

---

## 📝 Prerequisites

```bash
pip install pyspark delta-spark
```

---

## 🎯 Learning Path

1. **Start with:** `01_etl_pipeline.py` (basic ETL)
2. **Then try:** `04_data_quality_pipeline.py` (data validation)
3. **Next:** `05_medallion_architecture.py` (Delta Lake)
4. **Advanced:** `02_streaming_analytics.py`, `03_ml_churn_prediction.py`
5. **Expert:** `06_recommendation_engine.py`

---

**Each project is self-contained and runnable!** 🔥
