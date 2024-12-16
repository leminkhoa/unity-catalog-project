#!/bin/bash

echo "Setup schema..."
bash ./commands/setup-schemas.sh

echo "Set up raw tables..."
bash ./commands/setup-raw-tables.sh

echo "Set up volumes"
bash ./commands/setup-volumes.sh

echo "Set up functions..."
bash ./commands/setup-functions.sh

echo "All scripts completed."