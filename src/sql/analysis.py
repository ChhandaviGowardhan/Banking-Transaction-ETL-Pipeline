def run_sql_analysis(spark, df):
    # Register as temporary table
    df.createOrReplaceTempView("transactions")

    print("🔹 Total Spend Per User")
    result1 = spark.sql("""
        SELECT user_id, SUM(amount) AS total_spent
        FROM transactions
        GROUP BY user_id
        ORDER BY total_spent DESC
        LIMIT 5
    """)
    result1.show()

    print("🔹 Fraud Transactions Count")
    result2 = spark.sql("""
        SELECT is_fraud, COUNT(*) AS count
        FROM transactions
        GROUP BY is_fraud
    """)
    result2.show()

    print("🔹 High Value Transactions")
    result3 = spark.sql("""
        SELECT COUNT(*) AS high_value_count
        FROM transactions
        WHERE is_high_value = 1
    """)
    result3.show()

    return result1, result2, result3