"""
Project 4: Data Quality Pipeline
================================
Validate data quality with comprehensive checks.

Skills: Data validation, quality metrics, assertions

Run: spark-submit 04_data_quality_pipeline.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, when, isnan, isnull, lit,
    min, max, avg, stddev, countDistinct,
    regexp_extract, length
)
from datetime import datetime


def create_spark_session():
    """Create Spark session."""
    return SparkSession.builder \
        .appName("Data Quality Pipeline") \
        .getOrCreate()


def create_sample_data(spark):
    """Create sample data with quality issues for testing."""
    
    data = [
        # Good records
        (1, "Alice Johnson", "alice@email.com", 25, 50000.0, "2025-01-15"),
        (2, "Bob Smith", "bob@email.com", 35, 75000.0, "2025-01-16"),
        (3, "Charlie Brown", "charlie@email.com", 45, 95000.0, "2025-01-17"),
        # Null issues
        (4, None, "diana@email.com", 30, 60000.0, "2025-01-18"),
        (5, "Eve Wilson", None, 28, 55000.0, "2025-01-19"),
        # Invalid values
        (6, "Frank", "invalid-email", 150, 45000.0, "2025-01-20"),  # Invalid age, email
        (7, "Grace Lee", "grace@email.com", -5, 80000.0, "2025-01-21"),  # Negative age
        (8, "Henry Ford", "henry@email.com", 40, -10000.0, "2025-01-22"),  # Negative salary
        # Duplicates
        (1, "Alice Johnson", "alice@email.com", 25, 50000.0, "2025-01-15"),  # Duplicate
        # Format issues
        (9, "ivan", "IVAN@EMAIL.COM", 32, 70000.0, "2025-01-23"),  # Case issues
    ]
    
    columns = ["id", "name", "email", "age", "salary", "created_date"]
    
    return spark.createDataFrame(data, columns)


class DataQualityChecker:
    """Data Quality validation class."""
    
    def __init__(self, df, name="dataset"):
        self.df = df
        self.name = name
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def log_result(self, check_name, passed, details=""):
        """Log a check result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "check": check_name,
            "passed": passed,
            "details": details
        }
        self.results.append(result)
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        
        print(f"{status}: {check_name} - {details}")
    
    def check_not_null(self, column):
        """Check that column has no null values."""
        null_count = self.df.filter(col(column).isNull()).count()
        total = self.df.count()
        
        passed = null_count == 0
        pct = (null_count / total * 100) if total > 0 else 0
        
        self.log_result(
            f"Not Null: {column}",
            passed,
            f"{null_count} nulls ({pct:.1f}%)"
        )
        return self
    
    def check_unique(self, column):
        """Check that column values are unique."""
        total = self.df.count()
        distinct = self.df.select(column).distinct().count()
        duplicates = total - distinct
        
        passed = duplicates == 0
        
        self.log_result(
            f"Unique: {column}",
            passed,
            f"{duplicates} duplicates found"
        )
        return self
    
    def check_range(self, column, min_val, max_val):
        """Check that values are within expected range."""
        out_of_range = self.df.filter(
            (col(column) < min_val) | (col(column) > max_val)
        ).count()
        
        passed = out_of_range == 0
        
        self.log_result(
            f"Range [{min_val}, {max_val}]: {column}",
            passed,
            f"{out_of_range} values out of range"
        )
        return self
    
    def check_positive(self, column):
        """Check that values are positive."""
        negative = self.df.filter(col(column) < 0).count()
        
        passed = negative == 0
        
        self.log_result(
            f"Positive: {column}",
            passed,
            f"{negative} negative values"
        )
        return self
    
    def check_regex(self, column, pattern, description="pattern"):
        """Check that values match regex pattern."""
        non_matching = self.df.filter(
            ~col(column).rlike(pattern)
        ).count()
        
        # Exclude nulls from check
        non_null = self.df.filter(col(column).isNotNull())
        non_matching = non_null.filter(~col(column).rlike(pattern)).count()
        
        passed = non_matching == 0
        
        self.log_result(
            f"Regex ({description}): {column}",
            passed,
            f"{non_matching} values don't match"
        )
        return self
    
    def check_no_duplicates(self, columns):
        """Check for duplicate records based on columns."""
        total = self.df.count()
        distinct = self.df.dropDuplicates(columns).count()
        duplicates = total - distinct
        
        passed = duplicates == 0
        
        self.log_result(
            f"No Duplicates: {columns}",
            passed,
            f"{duplicates} duplicate rows"
        )
        return self
    
    def check_completeness(self, threshold=0.95):
        """Check overall completeness (% of non-null values)."""
        total_cells = self.df.count() * len(self.df.columns)
        null_cells = sum(
            self.df.filter(col(c).isNull()).count() 
            for c in self.df.columns
        )
        completeness = 1 - (null_cells / total_cells) if total_cells > 0 else 0
        
        passed = completeness >= threshold
        
        self.log_result(
            f"Completeness >= {threshold:.0%}",
            passed,
            f"Actual: {completeness:.1%}"
        )
        return self
    
    def get_summary(self):
        """Get summary of all checks."""
        return {
            "dataset": self.name,
            "total_checks": self.passed + self.failed,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": self.passed / (self.passed + self.failed) if (self.passed + self.failed) > 0 else 0,
            "results": self.results
        }
    
    def print_summary(self):
        """Print summary report."""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print(f"DATA QUALITY SUMMARY: {summary['dataset']}")
        print("=" * 60)
        print(f"Total Checks: {summary['total_checks']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1%}")
        print("=" * 60)
        
        if summary['failed'] > 0:
            print("\n⚠️ FAILED CHECKS:")
            for r in summary['results']:
                if not r['passed']:
                    print(f"  - {r['check']}: {r['details']}")


def compute_data_profile(df):
    """Compute data profile statistics."""
    print("\n" + "=" * 60)
    print("DATA PROFILE")
    print("=" * 60)
    
    print(f"\nTotal Records: {df.count()}")
    print(f"Total Columns: {len(df.columns)}")
    
    print("\nColumn Statistics:")
    print("-" * 50)
    
    for column in df.columns:
        col_type = dict(df.dtypes)[column]
        null_count = df.filter(col(column).isNull()).count()
        distinct_count = df.select(column).distinct().count()
        
        print(f"\n{column} ({col_type}):")
        print(f"  Nulls: {null_count}")
        print(f"  Distinct: {distinct_count}")
        
        if col_type in ['int', 'bigint', 'double', 'float']:
            stats = df.select(
                min(column).alias("min"),
                max(column).alias("max"),
                avg(column).alias("avg"),
                stddev(column).alias("stddev")
            ).first()
            print(f"  Min: {stats['min']}")
            print(f"  Max: {stats['max']}")
            print(f"  Avg: {stats['avg']:.2f}" if stats['avg'] else "  Avg: N/A")


def get_bad_records(df):
    """Extract records that failed quality checks."""
    print("\n" + "=" * 60)
    print("BAD RECORDS")
    print("=" * 60)
    
    # Records with null name
    bad_name = df.filter(col("name").isNull())
    print(f"\nNull names: {bad_name.count()}")
    
    # Records with invalid age
    bad_age = df.filter((col("age") < 0) | (col("age") > 120))
    print(f"Invalid age: {bad_age.count()}")
    
    # Records with invalid email
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    bad_email = df.filter(
        col("email").isNotNull() & ~col("email").rlike(email_pattern)
    )
    print(f"Invalid email: {bad_email.count()}")
    
    # Show all bad records
    all_bad = df.filter(
        col("name").isNull() |
        (col("age") < 0) | (col("age") > 120) |
        (col("salary") < 0) |
        (col("email").isNotNull() & ~col("email").rlike(email_pattern))
    )
    
    print(f"\nTotal bad records: {all_bad.count()}")
    all_bad.show()
    
    return all_bad


def main():
    """Main data quality pipeline."""
    print("\n" + "=" * 60)
    print("    DATA QUALITY PIPELINE PROJECT")
    print("=" * 60 + "\n")
    
    spark = create_spark_session()
    
    try:
        # Load data
        df = create_sample_data(spark)
        
        print("Input Data:")
        df.show()
        
        # Data profiling
        compute_data_profile(df)
        
        # Quality checks
        print("\n" + "=" * 60)
        print("RUNNING QUALITY CHECKS")
        print("=" * 60 + "\n")
        
        checker = DataQualityChecker(df, "customers")
        
        checker \
            .check_not_null("id") \
            .check_not_null("name") \
            .check_not_null("email") \
            .check_unique("id") \
            .check_range("age", 0, 120) \
            .check_positive("salary") \
            .check_regex("email", r'^[\w\.-]+@[\w\.-]+\.\w+$', "email format") \
            .check_no_duplicates(["id"]) \
            .check_completeness(0.90)
        
        checker.print_summary()
        
        # Get bad records
        bad_records = get_bad_records(df)
        
        # Save bad records for review
        if bad_records.count() > 0:
            bad_records.write.mode("overwrite").parquet("/tmp/dq_bad_records")
            print("\n⚠️ Bad records saved to /tmp/dq_bad_records")
        
        print("\n" + "=" * 60)
        print("    DATA QUALITY PIPELINE COMPLETED!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
