import os
from uuid import UUID

import pandas as pd
from typing import Optional

from pandas import DataFrame
from sgqlc.types import Variable, Arg, non_null, String, Int

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, ExecuteSqlQueryResponse, MaxMetricAttribute


class ExecuteSqlQueryResult:
    success = False
    code = None
    error = None
    df = None


class Data:
    """
    Helper for accessing data from the server.
    """

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient) -> None:
        self._auth_helper = auth_helper
        self._gql_client = gql_client

    def execute_sql_query(self, database_id: UUID, sql_query: str, row_limit: Optional[int]) -> ExecuteSqlQueryResult:
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

            execute_sql_query_response = result.execute_sql_query

            execute_sql_query_result = ExecuteSqlQueryResult()

            execute_sql_query_result.success = execute_sql_query_response.success
            execute_sql_query_result.error = execute_sql_query_response.error
            execute_sql_query_result.code = execute_sql_query_response.code

            if execute_sql_query_response.success:
                data = execute_sql_query_response.data

                columns = [column["name"] for column in data["columns"]]
                rows = [row["data"] for row in data["rows"]]

                df = pd.DataFrame(rows, columns=columns)

                execute_sql_query_result.df = df

            return execute_sql_query_result
        except Exception as e:
            execute_sql_query_result = ExecuteSqlQueryResult()

            execute_sql_query_result.success = False
            execute_sql_query_result.error = e
            execute_sql_query_result.code = 1000

            return execute_sql_query_result

    def get_dataset_id(self, dataset_name: str) -> Optional[UUID]:
        try:
            """
            dataset_name: the name of the dataset
            """
            query_args = {
                'datasetName': dataset_name,
            }

            query_vars = {
                'dataset_name': Arg(non_null(String)),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_dataset_id(
                dataset_name=Variable('dataset_name'),
            )

            result = self._gql_client.submit(operation, query_args)

            gql_response = result.get_dataset_id

            return gql_response
        except Exception as e:
            execute_sql_query_result = ExecuteSqlQueryResult()

            execute_sql_query_result.success = False
            execute_sql_query_result.error = e
            execute_sql_query_result.code = 1000

            return execute_sql_query_result

    def get_metric_attribute_by_name(self, dataset_id: UUID, rql_name: str) -> MaxMetricAttribute:
        try:
            """
            dataset_id: the UUID of the dataset
            rql_name: the fully qualified RQL name of the metric (e.g. transactions.sales)
            """
            query_args = {
                'datasetId': dataset_id,
                'rqlName': rql_name
            }

            query_vars = {
                'dataset_id': Arg(non_null(GQL_UUID)),
                'rql_name': Arg(non_null(String)),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_metric_attribute_by_name(
                dataset_id=Variable('dataset_id'),
                rql_name=Variable('rql_name'),
            )

            gql_query.type()
            gql_query.id()
            gql_query.name()
            gql_query.display_names()
            gql_query.display_format()
            gql_query.pluralized_display_name()
            gql_query.hide_from_user()
            gql_query.description()

            gql_query.db_metric_column()
            gql_query.agg_method()
            gql_query.row_level_filter()
            gql_query.positive_direction_up()
            gql_query.can_be_averaged()
            gql_query.not_additive()
            gql_query.growth_output_format()
            gql_query.hide_percentage_change()

            gql_query.plural()
            gql_query.headline_name()
            gql_query.is_favorite()

            gql_query.domain_entity()
            gql_query.domain_entity().id()
            gql_query.domain_entity().name()
            gql_query.domain_entity().db_table()

            result = self._gql_client.submit(operation, query_args)

            gql_response = result.get_metric_attribute_by_name

            return gql_response
        except Exception as e:
            execute_sql_query_result = ExecuteSqlQueryResult()

            execute_sql_query_result.success = False
            execute_sql_query_result.error = e
            execute_sql_query_result.code = 1000

            return execute_sql_query_result
