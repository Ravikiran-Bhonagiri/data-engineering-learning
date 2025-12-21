"""
Project 3: ML Churn Prediction
==============================
Build a customer churn prediction model with full MLlib pipeline.

Skills: MLlib, Pipelines, Feature Engineering, CrossValidator

Run: spark-submit 03_ml_churn_prediction.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    VectorAssembler, StringIndexer, StandardScaler,
    Imputer, OneHotEncoder
)
from pyspark.ml.classification import (
    LogisticRegression, RandomForestClassifier, GBTClassifier
)
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


def create_spark_session():
    """Create Spark session."""
    return SparkSession.builder \
        .appName("ML Churn Prediction") \
        .config("spark.sql.shuffle.partitions", 100) \
        .getOrCreate()


def create_sample_data(spark):
    """Create sample customer data for churn prediction."""
    
    data = [
        # customer_id, tenure_months, monthly_charges, total_charges, contract, payment_method, churned
        (1, 12, 65.5, 786.0, "Month-to-month", "Electronic check", 1),
        (2, 48, 89.9, 4315.2, "Two year", "Bank transfer", 0),
        (3, 6, 45.5, 273.0, "Month-to-month", "Electronic check", 1),
        (4, 24, 75.0, 1800.0, "One year", "Credit card", 0),
        (5, 3, 55.0, 165.0, "Month-to-month", "Electronic check", 1),
        (6, 60, 95.5, 5730.0, "Two year", "Bank transfer", 0),
        (7, 18, 70.0, 1260.0, "One year", "Credit card", 0),
        (8, 2, 50.0, 100.0, "Month-to-month", "Electronic check", 1),
        (9, 36, 85.0, 3060.0, "One year", "Bank transfer", 0),
        (10, 9, 60.0, 540.0, "Month-to-month", "Credit card", 1),
        (11, 72, 110.0, 7920.0, "Two year", "Bank transfer", 0),
        (12, 1, 45.0, 45.0, "Month-to-month", "Electronic check", 1),
        (13, 30, 80.0, 2400.0, "One year", "Credit card", 0),
        (14, 4, 55.5, 222.0, "Month-to-month", "Electronic check", 1),
        (15, 54, 100.0, 5400.0, "Two year", "Bank transfer", 0),
        # Add some with missing values
        (16, None, 70.0, None, "Month-to-month", "Credit card", 1),
        (17, 24, None, 1800.0, "One year", "Bank transfer", 0),
    ]
    
    columns = ["customer_id", "tenure_months", "monthly_charges", 
               "total_charges", "contract", "payment_method", "churned"]
    
    return spark.createDataFrame(data, columns)


def explore_data(df):
    """Explore and understand the data."""
    print("=" * 60)
    print("DATA EXPLORATION")
    print("=" * 60)
    
    print("\nSchema:")
    df.printSchema()
    
    print("\nSample Data:")
    df.show(5)
    
    print("\nStatistics:")
    df.describe().show()
    
    print("\nChurn Distribution:")
    df.groupBy("churned").count().show()
    
    print("\nContract Distribution:")
    df.groupBy("contract", "churned").count().orderBy("contract").show()
    
    print("\nMissing Values:")
    for c in df.columns:
        null_count = df.filter(col(c).isNull()).count()
        if null_count > 0:
            print(f"  {c}: {null_count} nulls")


def build_pipeline(numeric_cols, categorical_cols):
    """Build the ML pipeline with preprocessing and model."""
    
    stages = []
    
    # 1. Impute missing numeric values
    imputer = Imputer(
        inputCols=numeric_cols,
        outputCols=[f"{c}_imputed" for c in numeric_cols],
        strategy="median"
    )
    stages.append(imputer)
    
    # 2. Index categorical columns
    indexed_cols = []
    for cat_col in categorical_cols:
        indexer = StringIndexer(
            inputCol=cat_col,
            outputCol=f"{cat_col}_indexed",
            handleInvalid="keep"
        )
        stages.append(indexer)
        indexed_cols.append(f"{cat_col}_indexed")
    
    # 3. One-hot encode categorical
    encoded_cols = []
    for idx_col in indexed_cols:
        encoder = OneHotEncoder(
            inputCol=idx_col,
            outputCol=f"{idx_col}_encoded"
        )
        stages.append(encoder)
        encoded_cols.append(f"{idx_col}_encoded")
    
    # 4. Assemble all features
    feature_cols = (
        [f"{c}_imputed" for c in numeric_cols] +
        encoded_cols
    )
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features_raw",
        handleInvalid="skip"
    )
    stages.append(assembler)
    
    # 5. Scale features
    scaler = StandardScaler(
        inputCol="features_raw",
        outputCol="features",
        withStd=True,
        withMean=True
    )
    stages.append(scaler)
    
    # 6. Classifier (will be replaced during tuning)
    classifier = GBTClassifier(
        featuresCol="features",
        labelCol="churned",
        maxIter=20,
        seed=42
    )
    stages.append(classifier)
    
    return Pipeline(stages=stages), classifier


def train_with_cross_validation(pipeline, classifier, train_df):
    """Train model with hyperparameter tuning."""
    print("=" * 60)
    print("MODEL TRAINING (with Cross-Validation)")
    print("=" * 60)
    
    # Parameter grid
    paramGrid = ParamGridBuilder() \
        .addGrid(classifier.maxDepth, [3, 5, 7]) \
        .addGrid(classifier.stepSize, [0.1, 0.05]) \
        .build()
    
    # Evaluator
    evaluator = BinaryClassificationEvaluator(
        labelCol="churned",
        metricName="areaUnderROC"
    )
    
    # Cross-validator
    cv = CrossValidator(
        estimator=pipeline,
        estimatorParamMaps=paramGrid,
        evaluator=evaluator,
        numFolds=3,
        seed=42
    )
    
    print("Training with CrossValidator...")
    print(f"  Parameters to try: {len(paramGrid)}")
    print(f"  Folds: 3")
    
    cv_model = cv.fit(train_df)
    
    print(f"\nBest model AUC: {max(cv_model.avgMetrics):.4f}")
    
    return cv_model


def evaluate_model(model, test_df):
    """Evaluate model on test data."""
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    predictions = model.transform(test_df)
    
    # AUC
    evaluator = BinaryClassificationEvaluator(
        labelCol="churned",
        metricName="areaUnderROC"
    )
    auc = evaluator.evaluate(predictions)
    print(f"AUC: {auc:.4f}")
    
    # Accuracy (manual calculation)
    correct = predictions.filter(col("prediction") == col("churned")).count()
    total = predictions.count()
    accuracy = correct / total if total > 0 else 0
    print(f"Accuracy: {accuracy:.4f}")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    predictions.groupBy("churned", "prediction").count().orderBy("churned", "prediction").show()
    
    # Sample predictions
    print("\nSample Predictions:")
    predictions.select(
        "customer_id", "tenure_months", "contract", 
        "churned", "prediction", "probability"
    ).show(10, truncate=False)
    
    return predictions


def save_model(model, path="/tmp/churn_model"):
    """Save the trained model."""
    print(f"\nSaving model to {path}...")
    model.save(path)
    print("✅ Model saved!")


def main():
    """Main ML pipeline."""
    print("\n" + "=" * 60)
    print("    ML CHURN PREDICTION PROJECT")
    print("=" * 60 + "\n")
    
    spark = create_spark_session()
    
    try:
        # Load data
        df = create_sample_data(spark)
        
        # Explore
        explore_data(df)
        
        # Define columns
        numeric_cols = ["tenure_months", "monthly_charges", "total_charges"]
        categorical_cols = ["contract", "payment_method"]
        
        # Build pipeline
        pipeline, classifier = build_pipeline(numeric_cols, categorical_cols)
        
        # Split data
        train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
        print(f"\nTrain: {train_df.count()}, Test: {test_df.count()}")
        
        # Train with CV
        model = train_with_cross_validation(pipeline, classifier, train_df)
        
        # Evaluate
        evaluate_model(model.bestModel, test_df)
        
        # Save
        save_model(model)
        
        print("\n" + "=" * 60)
        print("    ML PIPELINE COMPLETED!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
