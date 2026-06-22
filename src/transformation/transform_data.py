from pyspark.sql.functions import col, hour, from_unixtime, when


def transform_data(df):
    # Convert transaction_time → timestamp
    df = df.withColumn(
        "transaction_timestamp",
        from_unixtime(col("transaction_time"))
    )

    # Extract hour
    df = df.withColumn(
        "transaction_hour",
        hour(col("transaction_timestamp"))
    )

    # High value transaction (threshold = 200)
    df = df.withColumn(
        "is_high_value",
        when(col("amount") > 200, 1).otherwise(0)
    )

    # Simulate transaction type
    df = df.withColumn(
        "transaction_type",
        when(col("amount") > 0, "debit").otherwise("credit")
    )

    return df