#!/bin/bash
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='lab'
export CATALOG_NAME=unity

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

$SPARK_HOME/bin/pyspark --name "local-uc-demo" \
    --master "local[*]" \
    --packages "io.delta:delta-spark_2.12:3.3.0,io.unitycatalog:unitycatalog-spark_2.12:0.2.1" \
    --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
    --conf "spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.${CATALOG_NAME}=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.${CATALOG_NAME}.uri=http://localhost:8080" \
    --conf "spark.sql.catalog.${CATALOG_NAME}.token=" \
    --conf "spark.sql.defaultCatalog=${CATALOG_NAME}" \
    --conf "spark.databricks.delta.catalog.update.enabled=true"

