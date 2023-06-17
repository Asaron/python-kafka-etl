#!/bin/bash
export SCHEMA=$(cat event/$1.avsc | tr -d '\n\t\r ')
export SCHEMA_JSON=$(echo '{"schema":""}' | jq --arg schema "$SCHEMA" '.schema = $schema')
echo $SCHEMA_JSON
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data $(echo $SCHEMA_JSON) localhost:8081//subjects/$1/versions