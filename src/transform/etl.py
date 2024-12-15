
def process_transaction(transaction_df, spark):

    transaction_df.createOrReplaceTempView("transaction")

    transaction_df = spark.sql("""
    SELECT 
        transaction_id,
        item.item_order,                       
        item.item_id,
        store,
        customer_id,
        staff_id,
        item.quantity,
        utc_dt
    FROM transaction
    LATERAL VIEW EXPLODE(transaction_items) AS item;
    """)

    spark.sql("DROP VIEW transaction")

    return transaction_df