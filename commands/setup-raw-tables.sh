#!/bin/bash

# Set variables
source .env

cd ~/data/app/uc/unitycatalog


# Create tables
bin/uc table create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.customers" \
    --columns "\
        customer_id STRING, \
        gender STRING, \
        first_name STRING, \
        last_name STRING, \
        email STRING, \
        yob DATE, \
        phone_number STRING, \
        job STRING, \
        address STRING, \
        first_transaction DATE, \
        membership STRING", \
        last_processed_ts TIMESTAMP \
    --format DELTA \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/customers" \
    --properties '{"domain": "customer"}'


# Create tables
bin/uc table create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.staffs" \
    --columns "\
        staff_id STRING, \
        gender STRING, \
        first_name STRING, \
        last_name STRING, \
        store_id STRING", \
        last_processed_ts TIMESTAMP \
    --format DELTA \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/staffs" \
    --properties '{"domain": "staff"}'


# Create tables
bin/uc table create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.stores" \
    --columns "\
        name STRING, \
        address STRING, \
        phone STRING, \
        email STRING, \
        last_processed_ts TIMESTAMP" \
    --format DELTA \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/stores" \
    --properties '{"domain": "store"}'

# Create tables
bin/uc table create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.products" \
    --columns "\
        product_id STRING, \
        category STRING, \
        product_name STRING, \
        unit_price LONG, \
        last_processed_ts TIMESTAMP" \
    --format DELTA \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/products" \
    --properties '{"domain": "product"}'


# Create tables
bin/uc table create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.transactions" \
    --columns "\
        transaction_id STRING, \
        item_id STRING, \
        item_order INT, \
        store STRING, \
        customer_id STRING, \
        staff_id STRING, \
        quantity INT, \
        utc_dt STRING, \
        last_processed_ts TIMESTAMP" \
    --format DELTA \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/transactions" \
    --properties '{"domain": "transaction"}'
