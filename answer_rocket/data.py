import os
from uuid import UUID

import pandas as pd
from typing import Optional

from sgqlc.types import Variable, Arg, non_null, String, Int

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, ExecuteSqlQueryResponse


class Data:
    """
    Helper for accessing data from the server.
    """

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient) -> None:
        self._auth_helper = auth_helper
        self._gql_client = gql_client

    def execute_sql_query(self, database_id: UUID, sql_query: str, row_limit: Optional[int]) -> ExecuteSqlQueryResponse:
        try:
            """
            sql_query: the SQL query to execute.
            row_limit: the optional row limit of the query results.
            """
            query_args = {
                'databaseId': database_id,
                'sqlQuery': sql_query,
                'rowLimit': row_limit,
            }

            query_vars = {
                'database_id': Arg(non_null(GQL_UUID)),
                'sql_query': Arg(non_null(String)),
                'row_limit': Arg(non_null(Int)),
            }

            operation = self._gql_client.query(variables=query_vars)

            execute_sql_query = operation.execute_sql_query(
                database_id=Variable('database_id'),
                sql_query=Variable('sql_query'),
                row_limit=Variable('row_limit'),
            )

            execute_sql_query.success()
            execute_sql_query.code()
            execute_sql_query.error()
            execute_sql_query.data()

            result = self._gql_client.submit(operation, query_args)

            return result.execute_sql_query
        except Exception as e:
            execute_sql_query_response = ExecuteSqlQueryResponse(
                json_data=None)

            execute_sql_query_response.success = False
            execute_sql_query_response.error = e
            execute_sql_query_response.code = 1000

            return execute_sql_query_response
