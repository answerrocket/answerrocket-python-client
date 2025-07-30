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
from answer_rocket.graphql.schema import UUID as GQL_UUID, GenerateVisualizationResponse, MaxMetricAttribute, \
    MaxDimensionEntity, MaxFactEntity, \
    MaxNormalAttribute, \
    MaxPrimaryAttribute, MaxReferenceAttribute, MaxCalculatedMetric, MaxDataset, MaxCalculatedAttribute, \
    MaxMutationResponse, JSON, RunSqlAiResponse, GroundedValueResponse, Dimension, \
    Metric, Dataset, DatasetDataInterval, Database, DatabaseSearchInput, PagingInput, PagedDatabases, \
    DatabaseTableSearchInput, PagedDatabaseTables, CreateDatasetFromTableResponse, DatasetSearchInput, PagedDatasets
from answer_rocket.graphql.sdk_operations import Operations
from answer_rocket.types import MaxResult, RESULT_EXCEPTION_CODE


def create_df_from_data(data: Dict[str, any]):
    """
    Create a pandas DataFrame from structured data dictionary.

    Parameters
    ----------
    data : Dict[str, any]
        A dictionary containing 'columns' and optionally 'rows' keys.
        The 'columns' key should contain a list of column dictionaries with 'name' keys.
        The 'rows' key should contain a list of row dictionaries with 'data' keys.

    Returns
    -------
    DataFrame
        A pandas DataFrame created from the input data. Returns an empty DataFrame
        with the same columns if the only row contains all NaN values.
    """
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
        """
        Execute an RQL query against a dataset and return results.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset to execute the query against.
        rql_query : str
            The RQL query string to execute.
        row_limit : Optional[int], optional
            Maximum number of rows to return in the query results.
        copilot_id : Optional[UUID], optional
            The UUID of the copilot. Defaults to the configured copilot_id.
        copilot_skill_id : Optional[UUID], optional
            The UUID of the copilot skill. Defaults to the configured copilot_skill_id.

        Returns
        -------
        ExecuteRqlQueryResult
            The result containing success status, error information, DataFrame, and RQL script response.
        """
        try:
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

    def get_database(self, database_id: UUID) -> Optional[Database]:
        """
        Retrieve a database by its ID.

        This method queries the backend for a database using the given unique identifier.
        If the database is found, it is returned as a `Database` object. If not found or
        if an error occurs during the query, `None` is returned.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to retrieve.

        Returns
        -------
        Database or None
            The database object if found, or `None` if not found or if an error occurs.
        """
        try:
            query_args = {
                'databaseId': str(database_id),
            }

            op = Operations.query.get_database

            result = self._gql_client.submit(op, query_args)

            return result.get_database
        except Exception as e:
            return None

    def get_databases(self, search_input: Optional[DatabaseSearchInput]=None, paging: Optional[PagingInput]=None) -> PagedDatabases:
        """
        Retrieve databases based on optional search and paging criteria.

        If no `search_input` or `paging` is provided, default values will be used.

        Parameters
        ----------
        search_input : DatabaseSearchInput, optional
            An object specifying the search criteria for databases.
            If None, no filters are applied
        paging : PagingInput, optional
            An object specifying pagination details such as page number and page size.
            If None, defaults to page 1 with a page size of 100.

        Returns
        -------
        PagedDatabases
            A paged collection of databases. Returns an empty `PagedDatabases` instance if an error occurs during retrieval.

        Notes
        -----
        This method uses a GraphQL client to submit a query to fetch the data.
        """
        try:
            if not search_input:
                search_input = DatabaseSearchInput(
                    name_contains=None,
                )

            if not paging:
                paging = PagingInput(
                    page_num=1,
                    page_size=100
                )

            query_args = {
                'searchInput': search_input.__to_json_value__(),
                'paging': paging.__to_json_value__()
            }

            op = Operations.query.get_databases

            result = self._gql_client.submit(op, query_args)

            return result.get_databases
        except Exception as e:
            return PagedDatabases()

    def get_database_tables(self, database_id: UUID, search_input: Optional[DatabaseTableSearchInput]=None, paging: Optional[PagingInput]=None) -> PagedDatabaseTables:
        """
        Retrieve database tables based on optional search and paging criteria.

        If no `search_input` or `paging` is provided, default values will be used.

        Parameters
        ----------
        database_id : UUID
            The database_id that contains the tables
        search_input : DatabaseTableSearchInput, optional
            An object specifying the search criteria for the tables.
            If None, no filters are applied
        paging : PagingInput, optional
            An object specifying pagination details such as page number and page size.
            If None, defaults to page 1 with a page size of 100.

        Returns
        -------
        PagedDatabaseTables
            A paged collection of database tables. Returns an empty `PagedDatabaseTables` instance if an error occurs during retrieval.

        Notes
        -----
        This method uses a GraphQL client to submit a query to fetch the data.
        """
        try:
            if not search_input:
                search_input = DatabaseTableSearchInput(
                    name_contains=None,
                )

            if not paging:
                paging = PagingInput(
                    page_num=1,
                    page_size=100
                )

            query_args = {
                'databaseId': str(database_id),
                'searchInput': search_input.__to_json_value__(),
                'paging': paging.__to_json_value__()
            }

            op = Operations.query.get_database_tables

            result = self._gql_client.submit(op, query_args)

            return result.get_database_tables
        except Exception as e:
            return PagedDatabaseTables()

    def get_datasets(self, search_input: Optional[DatasetSearchInput]=None, paging: Optional[PagingInput]=None) -> PagedDatasets:
        """
        Retrieve datasets based on optional search and paging criteria.

        If no `search_input` or `paging` is provided, default values will be used.

        Parameters
        ----------
        search_input : DatasetSearchInput, optional
            An object specifying the search criteria for datasets.
            If None, no filters are applied
        paging : PagingInput, optional
            An object specifying pagination details such as page number and page size.
            If None, defaults to page 1 with a page size of 100.

        Returns
        -------
        PagedDataset
            A paged collection of datasets. Returns an empty `PagedDataset` instance if an error occurs during retrieval.

        Notes
        -----
        This method uses a GraphQL client to submit a query to fetch the data.
        """
        try:
            if not search_input:
                search_input = DatasetSearchInput(
                    name_contains=None,
                )

            if not paging:
                paging = PagingInput(
                    page_num=1,
                    page_size=100
                )

            if hasattr(search_input, "database_id") and search_input.database_id:
                search_input.database_id = str(search_input.database_id)

            query_args = {
                'searchInput': search_input.__to_json_value__(),
                'paging': paging.__to_json_value__()
            }

            op = Operations.query.get_datasets

            result = self._gql_client.submit(op, query_args)

            return result.get_datasets
        except Exception as e:
            return PagedDatasets(0, [])

    def get_dataset_id(self, dataset_name: str) -> Optional[UUID]:
        """
        Retrieve the UUID of a dataset by its name.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset to look up.

        Returns
        -------
        Optional[UUID]
            The UUID of the dataset if found, otherwise None.
        """
        try:
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
        """
        Retrieve a dataset by its UUID with optional dimension values.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset to retrieve.
        copilot_id : Optional[UUID], optional
            The UUID of the copilot. Defaults to the configured copilot_id.
        include_dim_values : bool, optional
            Whether to include dimension values in the response. Defaults to False.

        Returns
        -------
        Optional[MaxDataset]
            The dataset object if found, otherwise None.
        """
        try:
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

            gql_query.dimensions()
            gql_query.metrics()

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

    def get_dataset2(self, dataset_id: UUID) -> Optional[Dataset]:
        """
        Retrieve a dataset by its ID.

        This method queries the backend for a dataset using the given unique identifier.
        If the dataset is found, it is returned as a `Dataset` object. If not found or
        if an error occurs during the query, `None` is returned.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to retrieve.

        Returns
        -------
        Dataset or None
            The dataset object if found, or `None` if not found or if an error occurs.
        """
        try:
            query_args = {
                'datasetId': str(dataset_id),
            }

            op = Operations.query.get_dataset2

            result = self._gql_client.submit(op, query_args)

            return result.get_dataset2
        except Exception as e:
            return None

    def get_domain_object_by_name(self, dataset_id: UUID, rql_name: str) -> DomainObjectResult:
        """
        Retrieve a domain object by its RQL name within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the domain object.
        rql_name : str
            The fully qualified RQL name of the domain object 
            (e.g. 'transactions.sales', 'transactions', 'net_sales').

        Returns
        -------
        DomainObjectResult
            The result containing success status, error information, and the domain object if found.
        """
        try:
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
        """
        Retrieve a domain object by its ID within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the domain object.
        domain_object_id : str
            The domain object ID (e.g. 'transactions__sales').

        Returns
        -------
        DomainObjectResult
            The result containing success status, error information, and the domain object if found.
        """
        try:
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

    def update_database_name(self, database_id: UUID, name: str) -> MaxMutationResponse:
        """
        Update the name of a database.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to be updated.
        name : str
            The new name to assign to the database. Must be a non-empty string.
            This name is typically used for display purposes in the UI or SDK.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated database name.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'name': name,
        }

        op = Operations.mutation.update_database_name
        result = self._gql_client.submit(op, mutation_args)

        return result.update_database_name

    def update_database_description(self, database_id: UUID, description: Optional[str]) -> MaxMutationResponse:
        """
        Update the description of a database.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to be updated.
        description : str or None
            A new description for the database. This can be any free-form text.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated database description.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'description': description,
        }

        op = Operations.mutation.update_database_description
        result = self._gql_client.submit(op, mutation_args)

        return result.update_database_description

    def update_database_llm_description(self, database_id: UUID, llm_description: Optional[str]) -> MaxMutationResponse:
        """
        Update the LLM-specific description of a database.

        This description is intended to provide context or metadata optimized for use by
        large language models (LLMs), such as for query generation or schema understanding.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to be updated.
        llm_description : str or None
            A natural-language description of the database, written to assist LLMs.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated LLM description.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'llmDescription': llm_description,
        }

        op = Operations.mutation.update_database_llm_description
        result = self._gql_client.submit(op, mutation_args)

        return result.update_database_llm_description

    def update_database_mermaid_er_diagram(self, database_id: UUID, mermaid_er_diagram: Optional[str]) -> MaxMutationResponse:
        """
        Update the Mermaid.js ER diagram representation for a database.

        This diagram can be used to visually describe the entity-relationship structure of the database,
        and is formatted using the Mermaid.js syntax.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to be updated.
        mermaid_er_diagram : str or None
            A string containing a Mermaid.js ER diagram definition.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated ER diagram information.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'mermaidErDiagram': mermaid_er_diagram,
        }

        op = Operations.mutation.update_database_mermaid_er_diagram
        result = self._gql_client.submit(op, mutation_args)

        return result.update_database_mermaid_er_diagram

    def update_database_kshot_limit(self, database_id: UUID, kshot_limit: int) -> MaxMutationResponse:
        """
        Update the k-shot limit for a database.

        The k-shot limit defines the maximum number of example rows to be used when generating
        prompts, previews, or training examples involving this database.

        Parameters
        ----------
        database_id : UUID
            The unique identifier of the database to be updated.
        kshot_limit : int
            The maximum number of rows (k-shot examples) to include. Must be a non-negative integer.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated k-shot limit.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'kShotLimit': kshot_limit,
        }

        op = Operations.mutation.update_database_kshot_limit
        result = self._gql_client.submit(op, mutation_args)

        return result.update_database_kshot_limit

    def reload_dataset(self, dataset_id: Optional[UUID] = None, database_id: Optional[UUID] = None, table_names: Optional[List[str]] = None) -> MaxMutationResponse:
        """
        Reload a dataset to refresh its metadata and structure.

        Parameters
        ----------
        dataset_id : Optional[UUID], optional
            The UUID of the dataset to reload.
        database_id : Optional[UUID], optional
            The UUID of the database containing tables to reload.
        table_names : Optional[List[str]], optional
            List of specific table names to reload.

        Returns
        -------
        MaxMutationResponse
            The result of the reload operation, or None if an error occurs.
        """
        try:
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

    def update_dataset_name(self, dataset_id: UUID, name: str) -> MaxMutationResponse:
        """
        Update the name of a dataset using its unique identifier.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        name : str
            The new name to assign to the dataset.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated dataset information.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'name': name,
        }

        op = Operations.mutation.update_dataset_name
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_name

    def update_dataset_description(self, dataset_id: UUID, description: Optional[str]) -> MaxMutationResponse:
        """
        Update the description of a dataset using its unique identifier.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        description : str
            The new description to assign to the dataset.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated dataset information.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'description': description,
        }

        op = Operations.mutation.update_dataset_description
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_description

    def update_dataset_date_range(self, dataset_id: UUID, min_date: Optional[str], max_date: Optional[str]) -> MaxMutationResponse:
        """
        Update the minimum and/or maximum date range for a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        min_date : str or None
            The new minimum date for the dataset in ISO 8601 format (e.g., "2023-01-01").
            If provided and missing a time component, "T00:00:00Z" will be appended.
        max_date : str or None
            The new maximum date for the dataset in ISO 8601 format (e.g., "2023-12-31").
            If provided and missing a time component, "T00:00:00Z" will be appended.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated dataset date range.
        """
        min_date_arg = min_date
        max_date_arg = max_date

        if min_date_arg and "Z" not in min_date_arg:
            min_date_arg += "T00:00:00Z"

        if max_date_arg and "Z" not in max_date_arg:
            max_date_arg += "T00:00:00Z"

        mutation_args = {
            'datasetId': str(dataset_id),
            'datasetMinDate': min_date_arg,
            'datasetMaxDate': max_date_arg,
        }

        op = Operations.mutation.update_dataset_date_range
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_date_range

    def update_dataset_data_interval(self, dataset_id: UUID, data_interval: Optional[DatasetDataInterval]) -> MaxMutationResponse:
        """
        Update the data interval setting for a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        data_interval : DatasetDataInterval or None
            The new data interval to assign to the dataset. Valid values are:

            - 'DATE'     : Daily data
            - 'WEEK'     : Weekly data
            - 'MONTH'    : Monthly data
            - 'QUARTER'  : Quarterly data
            - 'YEAR'     : Yearly data

            If None, the data interval will be set to DATE on the backend

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated dataset data interval.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'dataInterval': data_interval,
        }

        op = Operations.mutation.update_dataset_data_interval
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_data_interval

    def update_dataset_misc_info(self, dataset_id: UUID, misc_info: Optional[str]) -> MaxMutationResponse:
        """
        Update the miscellaneous information associated with a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        misc_info : str or None
            Arbitrary additional information to associate with the dataset.
            Can be any string, such as notes, metadata, or descriptive text.
            If None, the existing misc info may be cleared or left unchanged.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated dataset information.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'miscInfo': misc_info,
        }

        op = Operations.mutation.update_dataset_misc_info
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_misc_info

    def update_dataset_source(self, dataset_id: UUID, source_table: str, source_sql: Optional[str] = None, derived_table_alias: Optional[str] = None) -> MaxMutationResponse:
        """
        Update the source table configuration for a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset to update.
        source_table : str
            The name of the source table.
        source_sql : Optional[str], optional
            Custom SQL for the source table. Defaults to None.
        derived_table_alias : Optional[str], optional
            Alias for derived table queries. Defaults to None.

        Returns
        -------
        MaxMutationResponse
            The result of the update operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'sourceTable': source_table,
            'sourceSql': source_sql,
            'derivedTableAlias': derived_table_alias,
        }

        op = Operations.mutation.update_dataset_source
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_source

    def update_dataset_query_row_limit(self, dataset_id: UUID, query_row_limit: Optional[int]) -> MaxMutationResponse:
        """
        Update the maximum number of rows that can be returned in queries for a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        query_row_limit : int or None
            The maximum number of rows allowed per query. Must be a positive integer if provided.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated row limit setting.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'queryRowLimit': query_row_limit,
        }

        op = Operations.mutation.update_dataset_query_row_limit
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_query_row_limit

    def update_dataset_use_database_casing(self, dataset_id: UUID, use_database_casing: bool) -> MaxMutationResponse:
        """
        Update whether the dataset should use the original database casing for field names.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        use_database_casing : bool
            If True, the dataset will preserve the original casing of field names as defined in the database.
            If False, field names may be normalized (e.g., lowercased or transformed) by the system.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation reflecting the updated casing preference.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'useDatabaseCasing': use_database_casing,
        }

        op = Operations.mutation.update_dataset_use_database_casing
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_use_database_casing

    def update_dataset_kshot_limit(self, dataset_id: UUID, kshot_limit: int) -> MaxMutationResponse:
        """
        Update the k-shot limit for the dataset, which controls the number of example rows used for processing or training.

        Parameters
        ----------
        dataset_id : UUID
            The unique identifier of the dataset to be updated.
        kshot_limit : int
            The maximum number of examples (k-shot limit) to use when sampling or displaying example data.
            Must be a non-negative integer.

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the updated k-shot limit.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'kShotLimit': kshot_limit,
        }

        op = Operations.mutation.update_dataset_kshot_limit
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset_kshot_limit

    def create_dataset(self, dataset: Dataset) -> MaxMutationResponse:
        """
        Create a new dataset with the specified configuration.

        Parameters
        ----------
        dataset : Dataset
            The dataset object containing all necessary metadata and configuration
            required to create the dataset (e.g., name, schema, source connection, etc.).

        Returns
        -------
        MaxMutationResponse
            The result of the GraphQL mutation containing the created dataset details.

        Examples
        --------
        Create a dataset with dimensions and metrics:

        >>> dataset = {
        ...     "datasetId": dataset_id,
        ...     "name": "test from sdk",
        ...     "databaseId": "f4a03916-3a85-4774-95f2-2184bcfa5893",
        ...     "description": "Distributor sales",
        ...     "sourceTable": "fact_distributor_sales",
        ...     "dataInterval": "date",
        ...     "miscInfo": None,
        ...     "datasetMinDate": None,
        ...     "datasetMaxDate": None,
        ...     "queryRowLimit": 100,
        ...     "useDatabaseCasing": False,
        ...     "kShotLimit": 3,
        ...     "dimensions": [
        ...         {
        ...             "id" : "date",
        ...             "name" : "date",
        ...             "description" : None,
        ...             "outputLabel" : "Date",
        ...             "isActive" : True,
        ...             "miscInfo" : None,
        ...             "dataType" : "date",
        ...             "sqlExpression" : "date",
        ...             "sqlSortExpression" : None,
        ...             "sampleLimit" : 10
        ...         },
        ...         {
        ...             "id" : "department",
        ...             "name" : "department",
        ...             "description" : None,
        ...             "outputLabel" : "Department",
        ...             "isActive" : True,
        ...             "miscInfo" : None,
        ...             "dataType" : "string",
        ...             "sqlExpression" : "department",
        ...             "sqlSortExpression" : None,
        ...             "sampleLimit" : 10
        ...         }
        ...     ],
        ...     "metrics": [
        ...         {
        ...             "id" : "sales_amt",
        ...             "name" : "sales",
        ...             "description" : None,
        ...             "outputLabel" : "Sales",
        ...             "isActive" : True,
        ...             "miscInfo" : None,
        ...             "dataType" : "number",
        ...             "metricType": "basic",
        ...             "displayFormat": "$,.2f",
        ...             "sqlAggExpression": "SUM(sales_amt)",
        ...             "sqlRowExpression": "sales_amt",
        ...             "growthType": "percent_change",
        ...             "growthFormat": ",.2%"
        ...         },
        ...         {
        ...             "id" : "tax_amt",
        ...             "name" : "tax",
        ...             "description" : None,
        ...             "outputLabel" : "Tax",
        ...             "isActive" : True,
        ...             "miscInfo" : None,
        ...             "dataType" : "number",
        ...             "metricType": "basic",
        ...             "displayFormat": "$,.2f",
        ...             "sqlAggExpression": "SUM(tax_amt)",
        ...             "sqlRowExpression": "tax_amt",
        ...             "growthType": "percent_change",
        ...             "growthFormat": ",.2%"
        ...         }
        ...     ]
        ... }
        >>> response = max.data.create_dataset(dataset)
        """
        mutation_args = {
            'dataset': dataset,
        }

        op = Operations.mutation.create_dataset
        result = self._gql_client.submit(op, mutation_args)

        return result.create_dataset

    def create_dataset_from_table(self, database_id: UUID, table_name: str) -> CreateDatasetFromTableResponse:
        """
        Create a new dataset from the specified table

        Parameters
        ----------
        database_id : UUID
            The database ID under which to create the dataset
        table_name : str
            The name of the database table from which to create the dataset

        Returns
        -------
        CreateDatasetFromTableResponse
            The result of the GraphQL mutation containing the created dataset details.
        """
        mutation_args = {
            'databaseId': str(database_id),
            'tableName': table_name
        }

        op = Operations.mutation.create_dataset_from_table
        result = self._gql_client.submit(op, mutation_args)

        return result.create_dataset_from_table

    def update_dataset(self, dataset: Dataset) -> MaxMutationResponse:
        """
        Update an existing dataset with new configuration.

        Parameters
        ----------
        dataset : Dataset
            The dataset object containing the updated configuration and metadata.

        Returns
        -------
        MaxMutationResponse
            The result of the update operation.
        """
        mutation_args = {
            'dataset': dataset,
        }

        op = Operations.mutation.update_dataset
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dataset

    def create_dimension(self, dataset_id: UUID, dimension: Dimension) -> MaxMutationResponse:
        """
        Create a new dimension within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset to add the dimension to.
        dimension : Dimension
            The dimension object containing the configuration and metadata.

        Returns
        -------
        MaxMutationResponse
            The result of the create operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'dimension': dimension,
        }

        op = Operations.mutation.create_dimension
        result = self._gql_client.submit(op, mutation_args)

        return result.create_dimension

    def update_dimension(self, dataset_id: UUID, dimension: Dimension) -> MaxMutationResponse:
        """
        Update an existing dimension within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the dimension.
        dimension : Dimension
            The dimension object containing the updated configuration and metadata.

        Returns
        -------
        MaxMutationResponse
            The result of the update operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'dimension': dimension,
        }

        op = Operations.mutation.update_dimension
        result = self._gql_client.submit(op, mutation_args)

        return result.update_dimension

    def delete_dimension(self, dataset_id: UUID, dimension_id: str) -> MaxMutationResponse:
        """
        Delete a dimension from a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the dimension.
        dimension_id : str
            The ID of the dimension to delete.

        Returns
        -------
        MaxMutationResponse
            The result of the delete operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'dimensionId': dimension_id,
        }

        op = Operations.mutation.delete_dimension
        result = self._gql_client.submit(op, mutation_args)

        return result.delete_dimension

    def create_metric(self, dataset_id: UUID, metric: Metric) -> MaxMutationResponse:
        """
        Create a new metric within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset to add the metric to.
        metric : Metric
            The metric object containing the configuration and metadata.

        Returns
        -------
        MaxMutationResponse
            The result of the create operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'metric': metric,
        }

        op = Operations.mutation.create_metric
        result = self._gql_client.submit(op, mutation_args)

        return result.create_metric

    def update_metric(self, dataset_id: UUID, metric: Metric) -> MaxMutationResponse:
        """
        Update an existing metric within a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the metric.
        metric : Metric
            The metric object containing the updated configuration and metadata.

        Returns
        -------
        MaxMutationResponse
            The result of the update operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'metric': metric,
        }

        op = Operations.mutation.update_metric
        result = self._gql_client.submit(op, mutation_args)

        return result.update_metric

    def delete_metric(self, dataset_id: UUID, metric_id: str) -> MaxMutationResponse:
        """
        Delete a metric from a dataset.

        Parameters
        ----------
        dataset_id : UUID
            The UUID of the dataset containing the metric.
        metric_id : str
            The ID of the metric to delete.

        Returns
        -------
        MaxMutationResponse
            The result of the delete operation.
        """
        mutation_args = {
            'datasetId': str(dataset_id),
            'metricId': metric_id,
        }

        op = Operations.mutation.delete_metric
        result = self._gql_client.submit(op, mutation_args)

        return result.delete_metric
