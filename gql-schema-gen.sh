#!/bin/bash
# This script updates the sgqlc schema.py file by running an introspection query to first generate schema.json.
# You must be running AR locally and pass the tenant id of a tenant you have loaded as an argument for
# this to work.  For example: bash gql-schema-gen.sh ricedemo
python -m sgqlc.introspection \
	-H "Authorization: Max-Internal" \
	-H "Max-Tenant: $1" \
	"http://localhost:8080/api/sdk/graphql" \
	schema.json

sgqlc-codegen schema schema.json answer_rocket/graphql/schema.py