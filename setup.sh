#!/bin/bash

echo "Setup schema..."
bash ./setup-schemas.sh

echo "Set up raw tables..."
bash ./setup-raw-tables.sh

echo "Set up volumes"
bash ./setup-volumes.sh

echo "Set up functions..."
bash ./setup-functions.sh

echo "All scripts completed."