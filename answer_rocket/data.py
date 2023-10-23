from typing import Optional
from uuid import UUID

import pandas as pd
from sgqlc.operation import Fragment
from sgqlc.types import Variable, Arg, non_null, String, Int

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, MaxMetricAttribute, MaxDomainObject, \
    MaxDimensionEntity, MaxFactEntity, MaxNormalAttribute, \
    MaxPrimaryAttribute, MaxReferenceAttribute, MaxCalculatedMetric


class MaxResult:
    success = False
    code = None
    error = None


class ExecuteSqlQueryResult(MaxResult):
    df = None


class DomainObjectResult(MaxResult):
    domain_object = None

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

    def get_domain_object_by_name(self, dataset_id: UUID, rql_name: str) -> DomainObjectResult:
        try:
            """
            dataset_id: the UUID of the dataset
            rql_name: the fully qualified RQL name of the domain object (e.g. transactions.sales, transactions, net_sales)
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

            gql_query = operation.get_domain_object_by_name(
                dataset_id=Variable('dataset_id'),
                rql_name=Variable('rql_name'),
            )

            self._create_domain_object_query(gql_query)

            result = self._gql_client.submit(operation, query_args)

            gql_response = result.get_domain_object_by_name

            domain_object_result = DomainObjectResult()

            domain_object_result.success = gql_response.success
            domain_object_result.error = gql_response.error
            domain_object_result.code = gql_response.code
            domain_object_result.domain_object = gql_response.domain_object

            return domain_object_result
        except Exception as e:
            domain_object_result = DomainObjectResult()

            domain_object_result.success = False
            domain_object_result.error = e
            domain_object_result.code = 1000

            return domain_object_result

    def get_domain_object(self, dataset_id: UUID, domain_object_id: str) -> DomainObjectResult:
        try:
            """
            dataset_id: the UUID of the dataset
            domain_object_id: the domain object ID domain object (e.g. transactions__sales)
            """
            query_args = {
                'datasetId': dataset_id,
                'domainObjectId': domain_object_id
            }

            query_vars = {
                'dataset_id': Arg(non_null(GQL_UUID)),
                'domain_object_id': Arg(non_null(String)),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_domain_object(
                dataset_id=Variable('dataset_id'),
                domain_object_id=Variable('domain_object_id'),
            )

            self._create_domain_object_query(gql_query)

            result = self._gql_client.submit(operation, query_args)

            gql_response = result.get_domain_object

            domain_object_result = DomainObjectResult()

            domain_object_result.success = gql_response.success
            domain_object_result.error = gql_response.error
            domain_object_result.code = gql_response.code
            domain_object_result.domain_object = gql_response.domain_object

            return domain_object_result
        except Exception as e:
            domain_object_result = DomainObjectResult()

            domain_object_result.success = False
            domain_object_result.error = e
            domain_object_result.code = 1000

            return domain_object_result

    def _create_domain_object_query(self, gql_query):
        gql_query.success()
        gql_query.code()
        gql_query.error()
        domain_object = gql_query.domain_object()

        # domain_object_frag = Fragment(MaxDomainObject, 'MaxDomainObjectFragment')
        # gql_query.domain_object.__fragment__(domain_object_frag)
        domain_object.type()
        domain_object.id()
        domain_object.description()
        domain_object.output_label()
        domain_object.synonyms()
        domain_object.output_label_plural()
        domain_object.hide_from_user()

        fact_entity_frag = Fragment(MaxFactEntity, 'MaxFactEntityFragment')
        self._add_domain_entity_fields(fact_entity_frag)
        domain_object.__fragment__(fact_entity_frag)

        dimension_entity_frag = Fragment(MaxDimensionEntity, 'MaxDimensionEntityFragment')
        self._add_domain_entity_fields(dimension_entity_frag)
        domain_object.__fragment__(dimension_entity_frag)

        normal_attribute_frag = Fragment(MaxNormalAttribute, 'MaxNormalAttributeFragment')
        self._add_domain_attribute_fields(normal_attribute_frag)
        self._add_dimension_attribute_fields(normal_attribute_frag)
        normal_attribute_frag.db_column()
        normal_attribute_frag.db_secondary_column()
        domain_object.__fragment__(normal_attribute_frag)

        primary_attribute_frag = Fragment(MaxPrimaryAttribute, 'MaxPrimaryAttributeFragment')
        self._add_domain_attribute_fields(primary_attribute_frag)
        self._add_dimension_attribute_fields(primary_attribute_frag)
        primary_attribute_frag.db_primary_key_columns()
        primary_attribute_frag.db_secondary_column()
        domain_object.__fragment__(primary_attribute_frag)

        reference_attribute_frag = Fragment(MaxReferenceAttribute, 'MaxReferenceAttributeFragment')
        self._add_domain_attribute_fields(reference_attribute_frag)
        self._add_dimension_attribute_fields(reference_attribute_frag)
        reference_attribute_frag.db_foreign_key_columns()
        reference_attribute_frag.referenced_dimension_entity_id()
        domain_object.__fragment__(reference_attribute_frag)

        metric_attribute_frag = Fragment(MaxMetricAttribute, 'MaxMetricAttributeFragment')
        self._add_domain_attribute_fields(metric_attribute_frag)
        metric_attribute_frag.db_metric_column()
        metric_attribute_frag.agg_method()
        metric_attribute_frag.is_row_level_filter()
        metric_attribute_frag.is_positive_direction_up()
        metric_attribute_frag.can_be_averaged()
        metric_attribute_frag.is_not_additive()
        metric_attribute_frag.growth_output_format()
        metric_attribute_frag.hide_percentage_change()
        domain_object.__fragment__(metric_attribute_frag)
        
        calc_metric_attribute_frag = Fragment(MaxCalculatedMetric, 'MaxCalculatedMetricFragment')
        # self._add_domain_object_fields(calc_metric_attribute_frag)
        calc_metric_attribute_frag.display_format()
        calc_metric_attribute_frag.rql()
        calc_metric_attribute_frag.agg_method()
        calc_metric_attribute_frag.is_positive_direction_up()
        calc_metric_attribute_frag.can_be_averaged()
        calc_metric_attribute_frag.is_not_additive()
        calc_metric_attribute_frag.growth_output_format()
        calc_metric_attribute_frag.hide_percentage_change()
        domain_object.__fragment__(calc_metric_attribute_frag)

    def _add_domain_entity_fields(self, fragment: Fragment):
        fragment.db_table()

    def _add_domain_object_fields(self, domain_object):
        domain_object.type()
        domain_object.id()
        domain_object.name()
        domain_object.description()
        domain_object.output_label()
        domain_object.synonyms()
        domain_object.output_label_plural()
        domain_object.hide_from_user()
    def _add_domain_attribute_fields(self, fragment: Fragment):
        fragment.display_format()
        fragment.headline_name()
        fragment.is_favorite()
        # fragment.domain_entity()

    def _add_dimension_attribute_fields(self, fragment: Fragment):
        fragment.default_filter_value()
        fragment.is_required_in_query()
