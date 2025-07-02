from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from uuid import UUID

import pandas as pd
from pandas import DataFrame
from sgqlc.operation import Fragment
from sgqlc.types import Variable, Arg, non_null, String, Int, list_of

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, GenerateVisualizationResponse, MaxMetricAttribute, MaxDimensionEntity, MaxFactEntity, \
    MaxNormalAttribute, \
    MaxPrimaryAttribute, MaxReferenceAttribute, MaxCalculatedMetric, MaxDataset, MaxCalculatedAttribute, \
    MaxMutationResponse, DateTime, RunMaxSqlGenResponse, JSON, RunSqlAiResponse, GroundedValueResponse
from answer_rocket.graphql.sdk_operations import Operations
from answer_rocket.types import MaxResult, RESULT_EXCEPTION_CODE

def create_df_from_data(data: Dict[str, any]):
    columns = [column["name"] for column in data["columns"]]
    rows = [row["data"] for row in data["rows"]] if "rows" in data else []

    df = pd.DataFrame(rows, columns=columns)

    if len(df) == 1 and df.isna().all().all():
        return df.iloc[0:0]  # Returns an empty DataFrame with the same columns
    else:
        return df

@dataclass
class ExecuteSqlQueryResult(MaxResult):
    df: DataFrame | None = None
    data = None     # deprecated -- use df instead

@dataclass
class ExecuteRqlQueryResult(MaxResult):
    df = None
    rql_script_response = None

@dataclass
class DomainObjectResult(MaxResult):
    domain_object = None

@dataclass
class RunMaxSqlGenResult(MaxResult):
    sql: str | None = None
    df: DataFrame | None = None
    row_limit: int | None = None
    data = None     # deprecated -- use df instead

@dataclass
class RunSqlAiResult(MaxResult):
    sql: str | None = None
    df: DataFrame | None = None
    rendered_prompt: str | None = None
    column_metadata_map: Dict[str, any] | None = None
    title: str | None = None
    explanation: str | None = None
    data = None,     # deprecated -- use df instead
    timing_info: Dict[str, any] | None = None
    prior_runs: List[RunSqlAiResult] = field(default_factory=list)


class Data:
    """
    Helper for accessing data from the server.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        self._gql_client = gql_client
        self._config = config
        self.copilot_id = self._config.copilot_id
        self.copilot_skill_id = self._config.copilot_skill_id

    def execute_sql_query(self, database_id: UUID, sql_query: str, row_limit: Optional[int] = None, copilot_id: Optional[UUID] = None, copilot_skill_id: Optional[UUID] = None) -> ExecuteSqlQueryResult:
        """
        Executes a SQL query against the provided database, and returns a dataframe

        Args:
            database_id (UUID): The UUID of the database.
            sql_query (str): The SQL query to execute.
            row_limit (Optional[int]: An optional row limit to apply to the SQL query.
            copilot_id (Optional[UUID], optional): The UUID of the copilot. Defaults to None.

        Returns:
            ExecuteSqlQueryResult: The result of the SQL execution process.
        """

        result = ExecuteSqlQueryResult()

        try:
            query_args = {
                'databaseId': database_id,
                'sqlQuery': sql_query,
                'rowLimit': row_limit,
                'copilotId': copilot_id or self.copilot_id,
                'copilotSkillId': copilot_skill_id or self.copilot_skill_id,
            }

            query_vars = {
                'database_id': Arg(non_null(GQL_UUID)),
                'sql_query': Arg(non_null(String)),
                'row_limit': Arg(Int),
                'copilot_id': Arg(GQL_UUID),
                'copilot_skill_id': Arg(GQL_UUID),
            }

            operation = self._gql_client.query(variables=query_vars)

            execute_sql_query = operation.execute_sql_query(
                database_id=Variable('database_id'),
                sql_query=Variable('sql_query'),
                row_limit=Variable('row_limit'),
                copilot_id=Variable('copilot_id'),
                copilot_skill_id=Variable('copilot_skill_id'),
            )

            execute_sql_query.success()
            execute_sql_query.code()
            execute_sql_query.error()
            execute_sql_query.data()

            gql_result = self._gql_client.submit(operation, query_args)

            execute_sql_query_response = gql_result.execute_sql_query

            result.success = execute_sql_query_response.success
            result.error = execute_sql_query_response.error
            result.code = execute_sql_query_response.code

            if execute_sql_query_response.success:
                data = execute_sql_query_response.data

                result.df = create_df_from_data(data)
                result.data = data

            return result
        except Exception as e:
            result.success = False
            result.code = RESULT_EXCEPTION_CODE
            result.error = str(e)

            return result

    def execute_rql_query(self, dataset_id: UUID, rql_query: str, row_limit: Optional[int] = None, copilot_id: Optional[UUID] = None, copilot_skill_id: Optional[UUID] = None) -> ExecuteRqlQueryResult:
        try:
            """
            dataset_id: the dataset_id of the dataset to execute against.
            rql_query: the RQL query to execute.
            row_limit: the optional row limit of the query results.
            copilot_id: the optional copilot ID.
            
            """
            query_args = {
                'datasetId': dataset_id,
                'rqlQuery': rql_query,
                'rowLimit': row_limit,
                'copilotId': copilot_id or self.copilot_id,
                'copilotSkillId': copilot_skill_id or self.copilot_skill_id,
            }

            query_vars = {
                'dataset_id': Arg(non_null(GQL_UUID)),
                'rql_query': Arg(non_null(String)),
                'row_limit': Arg(Int),
                'copilot_id': Arg(GQL_UUID),
                'copilot_skill_id': Arg(GQL_UUID),
            }

            operation = self._gql_client.query(variables=query_vars)

            execute_rql_query = operation.execute_rql_query(
                dataset_id=Variable('dataset_id'),
                rql_query=Variable('rql_query'),
                row_limit=Variable('row_limit'),
                copilot_id=Variable('copilot_id'),
                copilot_skill_id=Variable('copilot_skill_id'),
            )

            execute_rql_query.success()
            execute_rql_query.code()
            execute_rql_query.error()
            execute_rql_query.data()
            execute_rql_query.process_rql_script_response()

            result = self._gql_client.submit(operation, query_args)

            execute_rql_query_response = result.execute_rql_query

            execute_rql_query_result = ExecuteRqlQueryResult()

            execute_rql_query_result.success = execute_rql_query_response.success
            execute_rql_query_result.error = execute_rql_query_response.error
            execute_rql_query_result.code = execute_rql_query_response.code

            if execute_rql_query_response.success:
                data = execute_rql_query_response.data

                columns = [column["name"] for column in data["columns"]]
                rows = [row["data"] for row in data["rows"]] if "rows" in data else []

                df = pd.DataFrame(rows, columns=columns)

                execute_rql_query_result.df = df

            execute_rql_query_result.rql_script_response = execute_rql_query_response.process_rql_script_response

            return execute_rql_query_result
        except Exception as e:
            execute_rql_query_result = ExecuteRqlQueryResult()

            execute_rql_query_result.success = False
            execute_rql_query_result.error = e
            execute_rql_query_result.code = RESULT_EXCEPTION_CODE

            return execute_rql_query_result

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
            execute_sql_query_result.code = RESULT_EXCEPTION_CODE

            return execute_sql_query_result

    def get_dataset(self, dataset_id: UUID, copilot_id: Optional[UUID] = None, include_dim_values: bool = False) -> Optional[MaxDataset]:
        try:
            """
            dataset_id: the UUID of the dataset
            """
            query_args = {
                'datasetId': str(dataset_id),
                'copilotId': str(copilot_id) if copilot_id else str(self.copilot_id) if self.copilot_id else None
            }

            query_vars = {
                'dataset_id': Arg(non_null(GQL_UUID)),
                'copilot_id': Arg(GQL_UUID),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_dataset(
                dataset_id=Variable('dataset_id'),
                copilot_id=Variable('copilot_id'),
            )

            gql_query.dataset_id()
            gql_query.name()
            gql_query.description()
            gql_query.misc_info()
            gql_query.dimension_value_distribution_map()
            gql_query.date_range_boundary_attribute_id()
            gql_query.dimension_hierarchies()
            gql_query.metric_hierarchies()
            gql_query.domain_attribute_statistics()
            gql_query.default_performance_metric_id()
            gql_query.dataset_min_date()
            gql_query.dataset_max_date()
            gql_query.query_row_limit()
            gql_query.use_database_casing()

            database = gql_query.database()
            database.database_id()
            database.name()
            database.dbms()
            database.schema()

            tables = gql_query.tables()
            tables.name()
            columns = tables.columns()

            columns.name()
            columns.jdbc_type()
            columns.length()
            columns.precision()
            columns.scale()

            self._create_domain_object_query(gql_query.domain_objects(), include_dim_values)

            result = self._gql_client.submit(operation, query_args)

            dataset = result.get_dataset

            return dataset
        except Exception as e:
            return None

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

            gql_query.success()
            gql_query.code()
            gql_query.error()

            self._create_domain_object_query(gql_query.domain_object())

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
            domain_object_result.code = RESULT_EXCEPTION_CODE

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

            gql_query.success()
            gql_query.code()
            gql_query.error()

            self._create_domain_object_query(gql_query.domain_object())

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
            domain_object_result.code = RESULT_EXCEPTION_CODE

            return domain_object_result

    def get_grounded_value(self, dataset_id: UUID, value: str, domain_entity: Optional[str] = None, copilot_id: Optional[UUID] = None) -> GroundedValueResponse:
        """
        Gets grounded values for fuzzy matching against domain values.

        Args:
            dataset_id (UUID): The UUID of the dataset.
            value (str): The value to ground (single string).
            domain_entity (Optional[str], optional): The domain entity to search within. Can be "metrics", "dimensions", a specific domain attribute name, or None to search all. Defaults to None.
            copilot_id (Optional[UUID], optional): The UUID of the copilot. Defaults to None.

        Returns:
            GroundedValueResponse: The grounded value response from the GraphQL schema.
        """
        
        try:
            query_args = {
                'datasetId': dataset_id,
                'value': value,
                'domainEntity': domain_entity,
                'copilotId': copilot_id or self.copilot_id,
            }
    
            op = Operations.query.get_grounded_value
            result = self._gql_client.submit(op, query_args)
    
            return result.get_grounded_value
        except Exception as e:
            return None

    def run_max_sql_gen(self, dataset_id: UUID, pre_query_object: Dict[str, any], copilot_id: Optional[UUID] = None) -> RunMaxSqlGenResult:
        """
        Runs the SQL generation logic using the provided dataset and query object.

        Args:
            dataset_id (UUID): The UUID of the dataset.
            pre_query_object (Dict[str, any]): The pre-query object that describes the query.
            copilot_id (Optional[UUID], optional): The UUID of the copilot. Defaults to None.

        Returns:
            RunMaxSqlGenResult: The result of the SQL generation process.
        """

        result = RunMaxSqlGenResult()

        try:
            query_args = {
                'datasetId': str(dataset_id),
                'preQueryObject': pre_query_object,
                'copilotId': str(copilot_id) if copilot_id else str(self.copilot_id) if self.copilot_id else None
            }

            query_vars = {
                'dataset_id': Arg(non_null(GQL_UUID)),
                'pre_query_object': Arg(non_null(JSON)),
                'copilot_id': Arg(GQL_UUID),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.run_max_sql_gen(
                dataset_id=Variable('dataset_id'),
                pre_query_object=Variable('pre_query_object'),
                copilot_id=Variable('copilot_id'),
            )

            gql_query.success()
            gql_query.code()
            gql_query.error()
            gql_query.sql()
            gql_query.row_limit()
            gql_query.data()

            gql_result = self._gql_client.submit(operation, query_args)

            run_max_sql_gen_response = gql_result.run_max_sql_gen

            result.success = run_max_sql_gen_response.success
            result.error = run_max_sql_gen_response.error
            result.code = run_max_sql_gen_response.code

            if result.success:
                result.sql = run_max_sql_gen_response.sql
                result.df = create_df_from_data(run_max_sql_gen_response.data)
                result.row_limit = run_max_sql_gen_response.row_limit
                result.data = run_max_sql_gen_response.data

            return result
        except Exception as e:
            result.success = False
            result.code = RESULT_EXCEPTION_CODE
            result.error = str(e)

            return result

    def run_sql_ai(
            self,
            dataset_id: Optional[str | UUID] = None,
            question: str = "",
            model_override: Optional[str] = None,
            copilot_id: Optional[UUID] = None,
            dataset_ids: Optional[list[str | UUID]] = None,
            database_id: Optional[str | UUID] = None
    ) -> RunSqlAiResult:
        """
        Runs the SQL AI generation logic using the provided dataset and natural language question.

        Args:
            dataset_id (Optional[str | UUID]): The UUID of the dataset.
            question (str): The natural language question.
            model_override (Optional[str], optional): Optional LLM model override. Defaults to None.
            copilot_id (Optional[UUID], optional): The UUID of the copilot. Defaults to None.
            dataset_ids (Optional[list[str | UUID]]): The UUIDs of the datasets.
            database_id (Optional[str | UUID]): The UUID of the database.
        Returns:
            RunSqlAiResult: The result of the SQL AI generation process.
        """

        result = RunSqlAiResult()

        try:
            query_args = {
                'datasetId': str(dataset_id) if dataset_id else None,
                'datasetIds': [str(x) for x in dataset_ids] if dataset_ids else None,
                'databaseId': str(database_id) if database_id else None,
                'question': question,
                'modelOverride': model_override,
                'copilotId': str(copilot_id) if copilot_id else str(self.copilot_id) if self.copilot_id else None
            }

            query_vars = {
                'dataset_id': Arg(GQL_UUID),
                'dataset_ids': list_of(non_null(GQL_UUID)),
                'database_id': Arg(GQL_UUID),
                'question': Arg(non_null(String)),
                'model_override': Arg(String),
                'copilot_id': Arg(GQL_UUID),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.run_sql_ai(
                dataset_id=Variable('dataset_id'),
                dataset_ids=Variable('dataset_ids'),
                database_id=Variable('database_id'),
                question=Variable('question'),
                model_override=Variable('model_override'),
                copilot_id=Variable('copilot_id'),
            )

            gql_query.success()
            gql_query.code()
            gql_query.error()
            gql_query.rendered_prompt()
            gql_query.explanation()
            gql_query.title()
            gql_query.sql()
            gql_query.raw_sql()
            gql_query.data()
            gql_query.column_metadata_map()
            gql_query.timing_info()
            gql_query.prior_runs()
            gql_result = self._gql_client.submit(operation, query_args)

            run_sql_ai_response = gql_result.run_sql_ai

            def create_result(response: RunSqlAiResponse) -> RunSqlAiResult:
                run_sql_ai_result = RunSqlAiResult()

                run_sql_ai_result.success = response.success
                run_sql_ai_result.error = response.error
                run_sql_ai_result.code = response.code

                run_sql_ai_result.sql = response.sql
                run_sql_ai_result.raw_sql = response.raw_sql
                run_sql_ai_result.rendered_prompt = response.rendered_prompt
                run_sql_ai_result.column_metadata_map = response.column_metadata_map
                run_sql_ai_result.title = response.title
                run_sql_ai_result.explanation = response.explanation
                run_sql_ai_result.data = response.data
                run_sql_ai_result.timing_info = response.timing_info
                run_sql_ai_result.prior_runs = [create_result(x) for x in response.prior_runs] \
                    if hasattr(response, 'prior_runs') else []

                if run_sql_ai_result.success:
                    run_sql_ai_result.df = create_df_from_data(response.data)

                return run_sql_ai_result

            result = create_result(run_sql_ai_response)
        except Exception as e:
            result.success = False
            result.code = RESULT_EXCEPTION_CODE
            result.error = str(e)

        return result

    def generate_visualization(self, data: Dict, column_metadata_map: Dict) -> Optional[GenerateVisualizationResponse]:
        """
        Generates a HighchartsChart dynamic vis layout component based on provided data and metadata.

        data: The data to be visualized, can pass directly from the data result of run_sql_ai (the services expects a 'rows' key and a 'columns' key)
        column_metadata_map: The column metadata map from the run_sql_ai response

        Returns:
            A HighchartsChart dynamic vis layout component based on provided data and metadata.
        """
        try:
            query_args = {
                'data': data,
                'columnMetadataMap': column_metadata_map,
            }

            query_vars = {
                'data': Arg(non_null(JSON)),
                'column_metadata_map': Arg(non_null(JSON)),
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.generate_visualization(
                data=Variable('data'),
                column_metadata_map=Variable('column_metadata_map'),
            )

            gql_query.success()
            gql_query.code()
            gql_query.error()
            gql_query.visualization()
            result = self._gql_client.submit(operation, query_args)

            generate_visualization_response = result.generate_visualization

            return generate_visualization_response
        except Exception as e:
            return None

    def _create_domain_object_query(self, domain_object, include_dim_values: bool = False):
        # domain_object_frag = Fragment(MaxDomainObject, 'MaxDomainObjectFragment')
        # gql_query.domain_object.__fragment__(domain_object_frag)

        self._add_domain_object_fields(domain_object)

        fact_entity_frag = Fragment(MaxFactEntity, 'MaxFactEntityFragment')
        self._add_domain_entity_fields(fact_entity_frag, include_dim_values)
        domain_object.__fragment__(fact_entity_frag)

        dimension_entity_frag = Fragment(MaxDimensionEntity, 'MaxDimensionEntityFragment')
        self._add_domain_entity_fields(dimension_entity_frag, include_dim_values)
        dimension_entity_frag.archetype()
        domain_object.__fragment__(dimension_entity_frag)

        self._add_domain_attribute_fragments(domain_object, include_dim_values)

        calc_metric_attribute_frag = Fragment(MaxCalculatedMetric, 'MaxCalculatedMetricFragment')
        self._add_domain_object_fields(calc_metric_attribute_frag)
        calc_metric_attribute_frag.display_format()
        calc_metric_attribute_frag.rql()
        calc_metric_attribute_frag.sql()
        calc_metric_attribute_frag.sql_agg_expression()
        calc_metric_attribute_frag.agg_method()
        calc_metric_attribute_frag.is_positive_direction_up()
        calc_metric_attribute_frag.can_be_averaged()
        calc_metric_attribute_frag.is_not_additive()
        calc_metric_attribute_frag.growth_output_format()
        calc_metric_attribute_frag.hide_percentage_change()
        calc_metric_attribute_frag.simplified_data_type()
        calc_metric_attribute_frag.metric_type()
        domain_object.__fragment__(calc_metric_attribute_frag)

    def _add_domain_attribute_fragments(self, domain_object, include_dim_values: bool = False):
        self._add_domain_object_fields(domain_object)

        normal_attribute_frag = Fragment(MaxNormalAttribute, 'MaxNormalAttributeFragment')
        self._add_domain_attribute_fields(normal_attribute_frag)
        self._add_dimension_attribute_fields(normal_attribute_frag, include_dim_values)
        normal_attribute_frag.db_column()
        normal_attribute_frag.db_secondary_column()
        domain_object.__fragment__(normal_attribute_frag)

        primary_attribute_frag = Fragment(MaxPrimaryAttribute, 'MaxPrimaryAttributeFragment')
        self._add_domain_attribute_fields(primary_attribute_frag)
        self._add_dimension_attribute_fields(primary_attribute_frag, include_dim_values)
        primary_attribute_frag.db_primary_key_columns()
        primary_attribute_frag.db_secondary_column()
        domain_object.__fragment__(primary_attribute_frag)

        reference_attribute_frag = Fragment(MaxReferenceAttribute, 'MaxReferenceAttributeFragment')
        self._add_domain_attribute_fields(reference_attribute_frag)
        self._add_dimension_attribute_fields(reference_attribute_frag)
        reference_attribute_frag.db_foreign_key_columns()
        reference_attribute_frag.referenced_dimension_entity_id()
        domain_object.__fragment__(reference_attribute_frag)

        calculated_attribute_frag = Fragment(MaxCalculatedAttribute, 'MaxCalculatedAttributeFragment')
        self._add_domain_attribute_fields(calculated_attribute_frag)
        self._add_dimension_attribute_fields(calculated_attribute_frag, include_dim_values)
        calculated_attribute_frag.rql()
        domain_object.__fragment__(calculated_attribute_frag)

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
        metric_attribute_frag.sql_agg_expression()
        metric_attribute_frag.metric_type()
        domain_object.__fragment__(metric_attribute_frag)

    def _add_domain_entity_fields(self, fragment: Fragment, include_dim_values: bool = False):
        fragment.db_table()
        fragment.derived_table_sql()

        attributes = fragment.attributes()

        self._add_domain_attribute_fragments(attributes, include_dim_values)

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
        fragment.simplified_data_type()
        fragment.sql()

        # TODO: we do we want this?
        # fragment.domain_entity()
        # fragment.domain_entity().id()
        # fragment.domain_entity().name()

    def _add_dimension_attribute_fields(self, fragment: Fragment, include_dim_values: bool = False):
        fragment.default_filter_value()
        fragment.is_required_in_query()
        fragment.dimension_value_mapping_list()

        if include_dim_values:
            fragment.dimension_values()

        fragment.db_sort_column()

    def reload_dataset(self, dataset_id: Optional[UUID] = None, database_id: Optional[UUID] = None, table_names: Optional[List[str]] = None) -> MaxMutationResponse:
        try:
            """
            dataset_id: the UUID of the dataset
            """
            mutation_args = {
                'datasetId': str(dataset_id) if dataset_id is not None else None,
                'databaseId': str(database_id) if database_id is not None else None,
                'tableNames': table_names
            }

            mutation_vars = {
                'dataset_id': Arg(GQL_UUID),
                'database_id': Arg(GQL_UUID),
                'table_names': Arg(list_of(non_null(String))),
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.reload_dataset(
                dataset_id=Variable('dataset_id'),
                database_id=Variable('database_id'),
                table_names=Variable('table_names'),
            )

            result = self._gql_client.submit(operation, mutation_args)

            mutation_response = result.reload_dataset

            return mutation_response
        except Exception as e:
            return None

    def update_dataset_date_range(self, dataset_id: UUID, min_date: str, max_date: str):
        mutation_args = {
            'datasetId': dataset_id,
            'datasetMinDate': min_date,
            'datasetMaxDate': max_date,
        }

        mutation_vars = {
            'dataset_id': Arg(non_null(GQL_UUID)),
            'dataset_min_date': Arg(non_null(DateTime)),
            'dataset_max_date': Arg(non_null(DateTime)),
        }

        operation = self._gql_client.mutation(variables=mutation_vars)

        operation.update_dataset_date_range(
            dataset_id=Variable('dataset_id'),
            dataset_min_date=Variable('dataset_min_date'),
            dataset_max_date=Variable('dataset_max_date'),
        )

        result = self._gql_client.submit(operation, mutation_args)

        mutation_response = result.update_dataset_date_range

        return mutation_response
