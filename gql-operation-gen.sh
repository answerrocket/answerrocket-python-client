#!/bin/bash

python -m sgqlc.introspection \
	-H "Authorization: Max-Internal" \
	-H "Max-Tenant: $1" \
	"http://localhost:8080/api/sdk/graphql" \
	schema.json

# sgqlc-codegen accepts multiple input files but it doesn't quite work, if we don't merge them then we get
# redundant definitions of the top level Query/Mutation/Operation classes that overwrite each other.
cat answer_rocket/graphql/operations/[!_]*.gql > answer_rocket/graphql/operations/_merged.gql

sgqlc-codegen operation --schema schema.json \
  .schema \
  answer_rocket/graphql/sdk_operations.py \
  answer_rocket/graphql/operations/_merged.gql