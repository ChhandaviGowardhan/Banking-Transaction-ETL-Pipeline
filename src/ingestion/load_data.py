import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id

from src.cleaning.clean_data import clean_data
from src.transformation.transform_data import transform_data
from src.sql.analysis import run_sql_analysis
from src.anomaly_detection.detect_anomalies import detect_anomalies


def create_spark_session():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = SparkSession.builder \
        .appName("Bank Transaction ETL") \
        .master("local[*]") \
        .getOrCreate()

    return spark


def load_and_transform_data(spark, file_path):
    df = spark.read.csv(
        file_path,
        header=True,
        inferSchema=True
    )

    # Create transaction_id
    df = df.withColumn("transaction_id", monotonically_increasing_id())

    # Rename columns
    df = df.withColumnRenamed("Amount", "amount") \
           .withColumnRenamed("Class", "is_fraud") \
           .withColumnRenamed("Time", "transaction_time")

    # Create user_id
    df = df.withColumn("user_id", (col("transaction_id") % 1000))

    return df


if __name__ == "__main__":
    spark = create_spark_session()

    df = load_and_transform_data(spark, "data/raw/transactions.csv")

    df = clean_data(df)
    df = transform_data(df)

    print("Transformed Data Sample:")

    df.select(
        "transaction_id",
        "user_id",
        "amount",
        "transaction_hour",
        "is_high_value",
        "transaction_type"
    ).show(5)

    run_sql_analysis(spark, df)
    detect_anomalies(df)

    # =========================
    # ✅ FINAL WORKING SAVE (WINDOWS FIX)
    # =========================

    print("Saving using Pandas fallback...")

    # Convert Spark → Pandas
    pdf = df.toPandas()

    # Ensure folder exists
    os.makedirs("data/processed", exist_ok=True)

    # Save CSV
    output_path = "data/processed/transactions.csv"
    pdf.to_csv(output_path, index=False)

    print("✅ Data saved successfully at:", output_path)