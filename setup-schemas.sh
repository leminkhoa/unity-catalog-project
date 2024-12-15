#!/bin/bash

# Set variables
source .env

cd ~/data/app/uc/unitycatalog

# Create schema
bin/uc schema create \
    --catalog ${CATALOG} \
    --name ${RAW_SCHEMA} \
    --comment "This schema is used for storing raw datasets" \
    --properties '{"layer": "raw"}'