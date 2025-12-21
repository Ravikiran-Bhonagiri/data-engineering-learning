"""
Project 6: Recommendation Engine
================================
Build a product recommendation system using ALS (Alternating Least Squares).

Skills: MLlib ALS, Collaborative Filtering, Model Evaluation

Run: spark-submit 06_recommendation_engine.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, lit, count, avg
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder


def create_spark_session():
    """Create Spark session."""
    return SparkSession.builder \
        .appName("Recommendation Engine") \
        .config("spark.sql.crossJoin.enabled", "true") \
        .getOrCreate()


def create_sample_data(spark):
    """Create sample user-product ratings data."""
    
    # user_id, product_id, rating (1-5)
    ratings_data = [
        # User 1: Likes electronics
        (1, 101, 5.0), (1, 102, 4.0), (1, 103, 5.0), (1, 201, 2.0),
        # User 2: Likes books
        (2, 201, 5.0), (2, 202, 4.0), (2, 203, 5.0), (2, 101, 2.0),
        # User 3: Mixed preferences
        (3, 101, 4.0), (3, 201, 4.0), (3, 301, 5.0), (3, 102, 3.0),
        # User 4: Similar to User 1
        (4, 101, 5.0), (4, 102, 5.0), (4, 201, 1.0),
        # User 5: Similar to User 2
        (5, 201, 5.0), (5, 202, 5.0), (5, 101, 1.0),
        # User 6: New user with few ratings
        (6, 103, 4.0), (6, 302, 3.0),
        # User 7: Heavy user
        (7, 101, 3.0), (7, 102, 4.0), (7, 103, 2.0), 
        (7, 201, 5.0), (7, 202, 4.0), (7, 301, 3.0),
        # More users for better training
        (8, 101, 4.0), (8, 103, 5.0), (8, 301, 2.0),
        (9, 201, 4.0), (9, 203, 5.0), (9, 102, 3.0),
        (10, 301, 5.0), (10, 302, 4.0), (10, 101, 3.0),
    ]
    
    # Product catalog
    products_data = [
        (101, "Laptop", "Electronics"),
        (102, "Smartphone", "Electronics"),
        (103, "Headphones", "Electronics"),
        (201, "Python Programming", "Books"),
        (202, "Data Science Guide", "Books"),
        (203, "Machine Learning", "Books"),
        (301, "Coffee Maker", "Home"),
        (302, "Blender", "Home"),
    ]
    
    ratings = spark.createDataFrame(ratings_data, ["user_id", "product_id", "rating"])
    products = spark.createDataFrame(products_data, ["product_id", "name", "category"])
    
    return ratings, products


def explore_data(ratings, products):
    """Explore the ratings data."""
    print("\n" + "=" * 60)
    print("DATA EXPLORATION")
    print("=" * 60)
    
    print(f"\nTotal ratings: {ratings.count()}")
    print(f"Unique users: {ratings.select('user_id').distinct().count()}")
    print(f"Unique products: {ratings.select('product_id').distinct().count()}")
    
    print("\nRating distribution:")
    ratings.groupBy("rating").count().orderBy("rating").show()
    
    print("\nRatings per user:")
    ratings.groupBy("user_id").count().orderBy("count", ascending=False).show(5)
    
    print("\nProducts:")
    products.show()


def train_als_model(ratings):
    """Train ALS recommendation model."""
    print("\n" + "=" * 60)
    print("TRAINING ALS MODEL")
    print("=" * 60)
    
    # Split data
    train, test = ratings.randomSplit([0.8, 0.2], seed=42)
    print(f"Train: {train.count()}, Test: {test.count()}")
    
    # Build ALS model
    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="user_id",
        itemCol="product_id",
        ratingCol="rating",
        coldStartStrategy="drop",  # Handle new users/items
        nonnegative=True,  # Ensure non-negative ratings
        seed=42
    )
    
    # Train
    print("Training model...")
    model = als.fit(train)
    
    # Evaluate
    print("Evaluating...")
    predictions = model.transform(test)
    
    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating",
        predictionCol="prediction"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"RMSE: {rmse:.4f}")
    
    return model, train, test


def tune_hyperparameters(ratings):
    """Tune ALS hyperparameters with cross-validation."""
    print("\n" + "=" * 60)
    print("HYPERPARAMETER TUNING")
    print("=" * 60)
    
    als = ALS(
        userCol="user_id",
        itemCol="product_id",
        ratingCol="rating",
        coldStartStrategy="drop",
        nonnegative=True,
        seed=42
    )
    
    # Parameter grid
    paramGrid = ParamGridBuilder() \
        .addGrid(als.maxIter, [5, 10]) \
        .addGrid(als.regParam, [0.01, 0.1]) \
        .addGrid(als.rank, [5, 10]) \
        .build()
    
    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating",
        predictionCol="prediction"
    )
    
    cv = CrossValidator(
        estimator=als,
        estimatorParamMaps=paramGrid,
        evaluator=evaluator,
        numFolds=3
    )
    
    print(f"Testing {len(paramGrid)} parameter combinations with 3-fold CV...")
    cv_model = cv.fit(ratings)
    
    best_model = cv_model.bestModel
    print(f"\nBest Parameters:")
    print(f"  Rank: {best_model.rank}")
    print(f"  MaxIter: {best_model._java_obj.parent().getMaxIter()}")
    print(f"  RegParam: {best_model._java_obj.parent().getRegParam()}")
    
    print(f"\nBest RMSE: {min(cv_model.avgMetrics):.4f}")
    
    return best_model


def generate_recommendations(model, ratings, products, n_recommendations=3):
    """Generate product recommendations for all users."""
    print("\n" + "=" * 60)
    print(f"GENERATING TOP-{n_recommendations} RECOMMENDATIONS")
    print("=" * 60)
    
    # Get all users
    users = ratings.select("user_id").distinct()
    
    # Generate top N recommendations for each user
    recommendations = model.recommendForAllUsers(n_recommendations)
    
    # Explode recommendations
    exploded = recommendations.select(
        col("user_id"),
        explode(col("recommendations")).alias("rec")
    ).select(
        col("user_id"),
        col("rec.product_id"),
        col("rec.rating").alias("predicted_rating")
    )
    
    # Join with product info
    with_products = exploded.join(products, "product_id")
    
    print("Recommendations per user:")
    with_products.orderBy("user_id", col("predicted_rating").desc()).show(20, truncate=False)
    
    return with_products


def recommend_for_user(model, products, ratings, user_id, n=5):
    """Get recommendations for a specific user."""
    print(f"\n👤 Recommendations for User {user_id}:")
    
    # User's past ratings
    print(f"\nPast ratings:")
    user_ratings = ratings.filter(col("user_id") == user_id)
    user_ratings.join(products, "product_id") \
        .select("name", "category", "rating") \
        .orderBy(col("rating").desc()) \
        .show()
    
    # Generate recommendations
    user_df = ratings.sparkSession.createDataFrame([(user_id,)], ["user_id"])
    recs = model.recommendForUserSubset(user_df, n)
    
    exploded = recs.select(
        col("user_id"),
        explode(col("recommendations")).alias("rec")
    ).select(
        col("rec.product_id"),
        col("rec.rating").alias("predicted_rating")
    )
    
    print(f"Recommended products:")
    exploded.join(products, "product_id") \
        .select("name", "category", "predicted_rating") \
        .orderBy(col("predicted_rating").desc()) \
        .show()


def find_similar_products(model, products, product_id, n=3):
    """Find products similar to a given product."""
    print(f"\n📦 Products similar to Product {product_id}:")
    
    product_df = products.sparkSession.createDataFrame([(product_id,)], ["product_id"])
    
    similar = model.recommendForItemSubset(product_df, n + 1)  # +1 because it may include itself
    
    exploded = similar.select(
        col("product_id").alias("base_product"),
        explode(col("recommendations")).alias("rec")
    ).select(
        col("rec.user_id"),
        col("rec.rating")
    )
    
    # This gives users who might like this product
    # For true item similarity, use item factors
    item_factors = model.itemFactors
    print(f"\nItem latent factors sample:")
    item_factors.show(5)


def main():
    """Main recommendation engine pipeline."""
    print("\n" + "=" * 60)
    print("    RECOMMENDATION ENGINE PROJECT")
    print("=" * 60 + "\n")
    
    spark = create_spark_session()
    
    try:
        # Load data
        ratings, products = create_sample_data(spark)
        
        # Explore
        explore_data(ratings, products)
        
        # Train model
        model, train, test = train_als_model(ratings)
        
        # Tune hyperparameters (optional - can be slow)
        # tuned_model = tune_hyperparameters(ratings)
        
        # Generate recommendations
        all_recs = generate_recommendations(model, ratings, products)
        
        # Specific user recommendations
        recommend_for_user(model, products, ratings, user_id=1)
        recommend_for_user(model, products, ratings, user_id=6)
        
        # Similar products
        find_similar_products(model, products, product_id=101)
        
        # Save model
        model_path = "/tmp/recommendation_model"
        model.save(model_path)
        print(f"\n✅ Model saved to {model_path}")
        
        print("\n" + "=" * 60)
        print("    RECOMMENDATION ENGINE COMPLETED!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
