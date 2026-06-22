if __name__ == "__main__":
    spark = create_spark_session()

    df = load_and_transform_data(spark, "data/raw/transactions.csv")

    df = clean_data(df)

    df = transform_data(df)   # 👈 ADD THIS

    print("Transformed Data Sample:")
    df.select(
        "transaction_id",
        "user_id",
        "amount",
        "transaction_hour",
        "is_high_value",
        "transaction_type"
    ).show(5)
    