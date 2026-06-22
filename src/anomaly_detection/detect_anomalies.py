from pyspark.sql.functions import mean, stddev, col


def detect_anomalies(df):
    stats = df.select(
        mean("amount").alias("mean"),
        stddev("amount").alias("std")
    ).collect()[0]

    mean_val = stats["mean"]
    std_val = stats["std"]

    print(f"Mean: {mean_val}, StdDev: {std_val}")

    # Z-score calculation
    df = df.withColumn(
        "z_score",
        (col("amount") - mean_val) / std_val
    )

    # Flag anomalies
    anomalies = df.filter(col("z_score") > 3)

    print("Anomalies count:", anomalies.count())

    anomalies.select(
        "transaction_id",
        "user_id",
        "amount",
        "z_score"
    ).show(5)

    return anomalies