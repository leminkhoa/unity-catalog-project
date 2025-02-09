from pyspark.sql.functions import current_timestamp
from jinja2 import Template


def add_processing_ts(df):
    df = df.withColumn("last_processed_ts", current_timestamp())
    return df

def uc_path(catalog, schema, table):
    return f"{catalog}.{schema}.{table}"

def merge_table(df, uc_path: str, merge_columns: list, spark):
    # Create temporary view for the dataframe
    df.createOrReplaceTempView("source")

    # Define the Jinja2 template for the SQL query
    sql_template = """
    MERGE INTO {{ uc_path }} as target
    USING source as source
    ON {% for column in merge_columns %} target.{{ column }} = source.{{ column }} {% if not loop.last %} AND {% endif %} {% endfor %}
    WHEN MATCHED THEN
        UPDATE SET *
    WHEN NOT MATCHED THEN
        INSERT *
    """

    # Render the template with the provided values
    template = Template(sql_template)
    query = template.render(uc_path=uc_path, merge_columns=merge_columns)

    # Print the generated SQL query
    print(f"Query: {query}")

    # Execute the query
    result = spark.sql(query)

    # Clean up by dropping the temporary view
    spark.sql("DROP VIEW source")
    
    return result.show()
