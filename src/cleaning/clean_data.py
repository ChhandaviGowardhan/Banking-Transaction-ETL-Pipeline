from pyspark.sql.functions import col


def clean_data(df):
    print("Initial count:", df.count())

    # 1️⃣ Remove nulls in important columns
    df = df.dropna(subset=["transaction_id", "amount", "user_id"])

    # 2️⃣ Remove invalid transactions
    df = df.filter(col("amount") > 0)

    # 3️⃣ Remove duplicates
    df = df.dropDuplicates(["transaction_id"])

    print("Final count after cleaning:", df.count())

    return df