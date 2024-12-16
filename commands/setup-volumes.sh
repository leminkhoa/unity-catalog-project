#!/bin/bash

# Set variables
source .env

cd ~/data/app/uc/unitycatalog


# Create folder for storing volumes
mkdir -p "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/_volumes/txt_files"
mkdir -p "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/_volumes/json_files"

# Create volumes
bin/uc volume create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.json_files" \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/_volumes/json_files" \
    --comment "This volume is used to store json files";

bin/uc volume create \
    --full_name "${CATALOG}.${RAW_SCHEMA}.txt_files" \
    --storage_location "${STORAGE_FOLDER}/uc_${CATALOG}/${RAW_SCHEMA}/_volumes/txt_files" \
    --comment "This volume is used to store text files";
