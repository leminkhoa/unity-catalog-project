#!/bin/bash
# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

cd $UC_HOME

# Start UC server
bin/start-uc-server