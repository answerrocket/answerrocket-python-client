#!/bin/bash

python -m sgqlc.introspection \
	-H "Authorization: Max-Internal" \
	-H "Max-Tenant: $1" \
	"http://localhost:8080/api/sdk/graphql" \
	schema.json

sgqlc-codegen operation --schema schema.json \
  .schema \
  answer_rocket/graphql/sdk_operations.py \
  answer_rocket/graphql/operations/*.gql