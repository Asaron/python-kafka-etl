#!/bin/bash
export SCHEMA=$(cat event/$1.avsc | tr '\n' ' ' | sed 's/"/\\"/g')
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"schema": "'"$SCHEMA"'"}' http://localhost:8081/subjects/$1/versions