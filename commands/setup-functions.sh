#!/bin/bash

# Set variables
source .env

cd ~/data/app/uc/unitycatalog

bin/uc function create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.my_function" \
    --data_type INT \
    --input_params "a int, b int" \
    --def "c=a*b\nreturn c"