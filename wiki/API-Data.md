# answer_rocket.data

## Classes

### `ExecuteSqlQueryResult`

Result object for SQL query execution operations.


**Attributes:**

- **df** (`DataFrame | None`): The result of the SQL query as a pandas DataFrame.
- **data** (`deprecated`): Deprecated field. Use df instead for DataFrame results.

### `DomainObjectResult`

Result object for domain object retrieval operations.

### `RunMaxSqlGenResult`

Result object for Max SQL generation operations.


**Attributes:**

- **sql** (`str | None`): The generated SQL query string.
- **df** (`DataFrame | None`): The result of executing the generated SQL as a pandas DataFrame.
- **row_limit** (`int | None`): The row limit applied to the SQL query.
- **data** (`deprecated`): Deprecated field. Use df instead for DataFrame results.

### `RunSqlAiResult`

Result object for SQL AI generation operations.


**Attributes:**

- **sql** (`str | None`): The generated SQL query string.
- **df** (`DataFrame | None`): The result of executing the generated SQL as a pandas DataFrame.
- **rendered_prompt** (`str | None`): The rendered prompt used for the AI generation.
- **column_metadata_map** (`Dict[str, any] | None`): Metadata mapping for columns in the result.
- **title** (`str | None`): The generated title for the query result.
- **explanation** (`str | None`): An explanation of the generated SQL query.
- **data** (`deprecated`): Deprecated field. Use df instead for DataFrame results.
- **timing_info** (`Dict[str, any] | None`): Performance timing information for the operation.
- **prior_runs** (`List[[RunSqlAiResult](API-Types)]`): List of prior runs for comparison or iteration tracking.

### `Data`

Helper for accessing data from the server.

#### Methods

##### `__init__(self, config: [ClientConfig](API-Types), gql_client: GraphQlClient) -> None`

##### `execute_sql_query(self, database_id: UUID, sql_query: str, row_limit: Optional[int], copilot_id: Optional[UUID], copilot_skill_id: Optional[UUID]) -> [ExecuteSqlQueryResult](API-Types)`


Execute a SQL query against the provided database and return a dataframe.


**Parameters:**

- **database_id** (`UUID`): The UUID of the database.
- **sql_query** (`str`): The SQL query to execute.
- **row_limit** (`int`, optional): An optional row limit to apply to the SQL query.
- **copilot_id** (`UUID`, optional): The UUID of the copilot. Defaults to the configured copilot_id.
- **copilot_skill_id** (`UUID`, optional): The UUID of the copilot skill. Defaults to the configured copilot_skill_id.


**Returns:**

`[ExecuteSqlQueryResult](API-Types)` - The result of the SQL execution process.

##### `get_database(self, database_id: UUID) -> Optional[Database]`


Retrieve a database by its ID.

This method queries the backend for a database using the given unique identifier.
If the database is found, it is returned as a `Database` object. If not found or
if an error occurs during the query, `None` is returned.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to retrieve.


**Returns:**

`Database or None` - The database object if found, or `None` if not found or if an error occurs.

##### `get_databases(self, search_input: Optional[DatabaseSearchInput], paging: Optional[PagingInput]) -> PagedDatabases`


Retrieve databases based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **search_input** (`DatabaseSearchInput`, optional): An object specifying the search criteria for databases. If None, no filters are applied
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`PagedDatabases` - A paged collection of databases. Returns an empty `PagedDatabases` instance if an error occurs during retrieval.

##### `get_database_tables(self, database_id: UUID, search_input: Optional[DatabaseTableSearchInput], paging: Optional[PagingInput]) -> PagedDatabaseTables`


Retrieve database tables based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **database_id** (`UUID`): The database_id that contains the tables
- **search_input** (`DatabaseTableSearchInput`, optional): An object specifying the search criteria for the tables. If None, no filters are applied
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`PagedDatabaseTables` - A paged collection of database tables. Returns an empty `PagedDatabaseTables` instance if an error occurs during retrieval.

##### `get_database_kshots(self, database_id: UUID, search_input: Optional[DatabaseKShotSearchInput], paging: Optional[PagingInput]) -> PagedDatabaseKShots`


Retrieve database k-shots based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **database_id** (`UUID`): The database_id that contains the k-shots
- **search_input** (`DatabaseKShotSearchInput`, optional): An object specifying the search criteria for the k-shots. If None, no filters are applied
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`PagedDatabaseKShots` - A paged collection of database k-shots. Returns an empty `PagedDatabaseKShots` instance if an error occurs during retrieval.

##### `get_database_kshot_by_id(self, database_kshot_id: UUID) -> Optional[DatabaseKShot]`


Retrieve a database k-shot by its ID.

This method queries the backend for a database k-shot using the given unique identifier.
If the k-shot is found, it is returned as a `DatabaseKShot` object. If not found or
if an error occurs during the query, `None` is returned.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to retrieve.


**Returns:**

`DatabaseKShot or None` - The database k-shot object if found, or `None` if not found or if an error occurs.

##### `get_datasets(self, search_input: Optional[DatasetSearchInput], paging: Optional[PagingInput]) -> PagedDatasets`


Retrieve datasets based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **search_input** (`DatasetSearchInput`, optional): An object specifying the search criteria for datasets. If None, no filters are applied
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`PagedDataset` - A paged collection of datasets. Returns an empty `PagedDataset` instance if an error occurs during retrieval.

##### `get_dataset_id(self, dataset_name: str) -> Optional[UUID]`


Retrieve the UUID of a dataset by its name.


**Parameters:**

- **dataset_name** (`str`): The name of the dataset to look up.


**Returns:**

`Optional[UUID]` - The UUID of the dataset if found, otherwise None.

##### `get_dataset(self, dataset_id: UUID, copilot_id: Optional[UUID], include_dim_values: bool) -> Optional[MaxDataset]`


Retrieve a dataset by its UUID with optional dimension values.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset to retrieve.
- **copilot_id** (`Optional[UUID]`, optional): The UUID of the copilot. Defaults to the configured copilot_id.
- **include_dim_values** (`bool`, optional): Whether to include dimension values in the response. Defaults to False.


**Returns:**

`Optional[MaxDataset]` - The dataset object if found, otherwise None.

##### `get_dataset2(self, dataset_id: UUID) -> Optional[Dataset]`


Retrieve a dataset by its ID.

This method queries the backend for a dataset using the given unique identifier.
If the dataset is found, it is returned as a `Dataset` object. If not found or
if an error occurs during the query, `None` is returned.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to retrieve.


**Returns:**

`Dataset or None` - The dataset object if found, or `None` if not found or if an error occurs.

##### `get_domain_object_by_name(self, dataset_id: UUID, rql_name: str) -> [DomainObjectResult](API-Types)`


Retrieve a domain object by its RQL name within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the domain object.
- **rql_name** (`str`): The fully qualified RQL name of the domain object (e.g. 'transactions.sales', 'transactions', 'net_sales').


**Returns:**

`[DomainObjectResult](API-Types)` - The result containing success status, error information, and the domain object if found.

##### `get_domain_object(self, dataset_id: UUID, domain_object_id: str) -> [DomainObjectResult](API-Types)`


Retrieve a domain object by its ID within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the domain object.
- **domain_object_id** (`str`): The domain object ID (e.g. 'transactions__sales').


**Returns:**

`[DomainObjectResult](API-Types)` - The result containing success status, error information, and the domain object if found.

##### `get_grounded_value(self, dataset_id: UUID, value: str, domain_entity: Optional[str], copilot_id: Optional[UUID]) -> GroundedValueResponse`


Get grounded values for fuzzy matching against domain values.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset.
- **value** (`str`): The value to ground (single string).
- **domain_entity** (`str`, optional): The domain entity to search within. Can be "metrics", "dimensions", a specific domain attribute name, or None to search all. Defaults to None.
- **copilot_id** (`UUID`, optional): The UUID of the copilot. Defaults to the configured copilot_id.


**Returns:**

`GroundedValueResponse` - The grounded value response from the GraphQL schema.

##### `run_max_sql_gen(self, dataset_id: UUID, pre_query_object: Dict[(str, any)], copilot_id: UUID | None, execute_sql: bool | None) -> [RunMaxSqlGenResult](API-Types)`


Run the SQL generation logic using the provided dataset and query object.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset.
- **pre_query_object** (`Dict[str, any]`): The pre-query object that describes the query.
- **copilot_id** (`UUID`, optional): The UUID of the copilot. Defaults to the configured copilot_id.
- **execute_sql** (`bool`, optional): Whether the generated SQL should be executed. Defaults to True.


**Returns:**

`[RunMaxSqlGenResult](API-Types)` - The result of the SQL generation process.

##### `run_sql_ai(self, dataset_id: Optional[str | UUID], question: str, model_override: Optional[str], copilot_id: Optional[UUID], dataset_ids: Optional[list[str | UUID]], database_id: Optional[str | UUID]) -> [RunSqlAiResult](API-Types)`


Run the SQL AI generation logic using the provided dataset and natural language question.


**Parameters:**

- **dataset_id** (`str | UUID`, optional): The UUID of the dataset.
- **question** (`str`): The natural language question. Defaults to empty string.
- **model_override** (`str`, optional): Optional LLM model override. Defaults to None.
- **copilot_id** (`UUID`, optional): The UUID of the copilot. Defaults to the configured copilot_id.
- **dataset_ids** (`list[str | UUID]`, optional): The UUIDs of multiple datasets.
- **database_id** (`str | UUID`, optional): The UUID of the database.


**Returns:**

`[RunSqlAiResult](API-Types)` - The result of the SQL AI generation process.

##### `generate_visualization(self, data: Dict, column_metadata_map: Dict) -> Optional[GenerateVisualizationResponse]`


Generate a HighchartsChart dynamic vis layout component based on provided data and metadata.


**Parameters:**

- **data** (`Dict`): The data to be visualized. Can pass directly from the data result of run_sql_ai. The service expects a 'rows' key and a 'columns' key.
- **column_metadata_map** (`Dict`): The column metadata map from the run_sql_ai response.


**Returns:**

`GenerateVisualizationResponse | None` - A HighchartsChart dynamic vis layout component based on provided data and metadata. Returns None if an error occurs.

##### `update_database_name(self, database_id: UUID, name: str) -> [MaxMutationResponse](API-Types)`


Update the name of a database.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to be updated.
- **name** (`str`): The new name to assign to the database. Must be a non-empty string. This name is typically used for display purposes in the UI or SDK.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated database name.

##### `update_database_description(self, database_id: UUID, description: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the description of a database.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to be updated.
- **description** (`str or None`): A new description for the database. This can be any free-form text.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated database description.

##### `update_database_llm_description(self, database_id: UUID, llm_description: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the LLM-specific description of a database.

This description is intended to provide context or metadata optimized for use by
large language models (LLMs), such as for query generation or schema understanding.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to be updated.
- **llm_description** (`str or None`): A natural-language description of the database, written to assist LLMs.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated LLM description.

##### `update_database_mermaid_er_diagram(self, database_id: UUID, mermaid_er_diagram: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the Mermaid.js ER diagram representation for a database.

This diagram can be used to visually describe the entity-relationship structure of the database,
and is formatted using the Mermaid.js syntax.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to be updated.
- **mermaid_er_diagram** (`str or None`): A string containing a Mermaid.js ER diagram definition.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated ER diagram information.

##### `update_database_kshot_limit(self, database_id: UUID, kshot_limit: int) -> [MaxMutationResponse](API-Types)`


Update the k-shot limit for a database.

The k-shot limit defines the maximum number of example rows to be used when generating
prompts, previews, or training examples involving this database.


**Parameters:**

- **database_id** (`UUID`): The unique identifier of the database to be updated.
- **kshot_limit** (`int`): The maximum number of rows (k-shot examples) to include. Must be a non-negative integer.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated k-shot limit.

##### `reload_dataset(self, dataset_id: Optional[UUID], database_id: Optional[UUID], table_names: Optional[List[str]]) -> [MaxMutationResponse](API-Types)`


Reload a dataset to refresh its metadata and structure.


**Parameters:**

- **dataset_id** (`Optional[UUID]`, optional): The UUID of the dataset to reload.
- **database_id** (`Optional[UUID]`, optional): The UUID of the database containing tables to reload.
- **table_names** (`Optional[List[str]]`, optional): List of specific table names to reload.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the reload operation, or None if an error occurs.

##### `update_dataset_name(self, dataset_id: UUID, name: str) -> [MaxMutationResponse](API-Types)`


Update the name of a dataset using its unique identifier.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **name** (`str`): The new name to assign to the dataset.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated dataset information.

##### `update_dataset_description(self, dataset_id: UUID, description: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the description of a dataset using its unique identifier.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **description** (`str`): The new description to assign to the dataset.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated dataset information.

##### `update_dataset_date_range(self, dataset_id: UUID, min_date: Optional[str], max_date: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the minimum and/or maximum date range for a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **min_date** (`str or None`): The new minimum date for the dataset in ISO 8601 format (e.g., "2023-01-01"). If provided and missing a time component, "T00:00:00Z" will be appended.
- **max_date** (`str or None`): The new maximum date for the dataset in ISO 8601 format (e.g., "2023-12-31"). If provided and missing a time component, "T00:00:00Z" will be appended.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated dataset date range.

##### `update_dataset_data_interval(self, dataset_id: UUID, data_interval: Optional[DatasetDataInterval]) -> [MaxMutationResponse](API-Types)`


Update the data interval setting for a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **data_interval** (`DatasetDataInterval or None`): The new data interval to assign to the dataset. Valid values are: - 'DATE'     : Daily data - 'WEEK'     : Weekly data - 'MONTH'    : Monthly data - 'QUARTER'  : Quarterly data - 'YEAR'     : Yearly data If None, the data interval will be set to DATE on the backend


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated dataset data interval.

##### `update_dataset_misc_info(self, dataset_id: UUID, misc_info: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the miscellaneous information associated with a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **misc_info** (`str or None`): Arbitrary additional information to associate with the dataset. Can be any string, such as notes, metadata, or descriptive text. If None, the existing misc info may be cleared or left unchanged.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated dataset information.

##### `update_dataset_source(self, dataset_id: UUID, source_table: str, source_sql: Optional[str], derived_table_alias: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the source table configuration for a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset to update.
- **source_table** (`str`): The name of the source table.
- **source_sql** (`Optional[str]`, optional): Custom SQL for the source table. Defaults to None.
- **derived_table_alias** (`Optional[str]`, optional): Alias for derived table queries. Defaults to None.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the update operation.

##### `update_dataset_query_row_limit(self, dataset_id: UUID, query_row_limit: Optional[int]) -> [MaxMutationResponse](API-Types)`


Update the maximum number of rows that can be returned in queries for a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **query_row_limit** (`int or None`): The maximum number of rows allowed per query. Must be a positive integer if provided.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated row limit setting.

##### `update_dataset_use_database_casing(self, dataset_id: UUID, use_database_casing: bool) -> [MaxMutationResponse](API-Types)`


Update whether the dataset should use the original database casing for field names.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **use_database_casing** (`bool`): If True, the dataset will preserve the original casing of field names as defined in the database. If False, field names may be normalized (e.g., lowercased or transformed) by the system.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation reflecting the updated casing preference.

##### `update_dataset_kshot_limit(self, dataset_id: UUID, kshot_limit: int) -> [MaxMutationResponse](API-Types)`


Update the k-shot limit for the dataset, which controls the number of example rows used for processing or training.


**Parameters:**

- **dataset_id** (`UUID`): The unique identifier of the dataset to be updated.
- **kshot_limit** (`int`): The maximum number of examples (k-shot limit) to use when sampling or displaying example data. Must be a non-negative integer.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated k-shot limit.

##### `create_dataset(self, dataset: Dataset) -> [MaxMutationResponse](API-Types)`


Create a new dataset with the specified configuration.


**Parameters:**

- **dataset** (`Dataset`): The dataset object containing all necessary metadata and configuration required to create the dataset (e.g., name, schema, source connection, etc.).


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the created dataset details.

##### `create_dataset_from_table(self, database_id: UUID, table_name: str) -> CreateDatasetFromTableResponse`


Create a new dataset from the specified table


**Parameters:**

- **database_id** (`UUID`): The database ID under which to create the dataset
- **table_name** (`str`): The name of the database table from which to create the dataset


**Returns:**

`CreateDatasetFromTableResponse` - The result of the GraphQL mutation containing the created dataset details.

##### `create_dimension(self, dataset_id: UUID, dimension: Dimension) -> [MaxMutationResponse](API-Types)`


Create a new dimension within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset to add the dimension to.
- **dimension** (`Dimension`): The dimension object containing the configuration and metadata.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the create operation.

##### `update_dimension(self, dataset_id: UUID, dimension: Dimension) -> [MaxMutationResponse](API-Types)`


Update an existing dimension within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the dimension.
- **dimension** (`Dimension`): The dimension object containing the updated configuration and metadata.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the update operation.

##### `delete_dimension(self, dataset_id: UUID, dimension_id: str) -> [MaxMutationResponse](API-Types)`


Delete a dimension from a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the dimension.
- **dimension_id** (`str`): The ID of the dimension to delete.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the delete operation.

##### `create_metric(self, dataset_id: UUID, metric: Metric) -> [MaxMutationResponse](API-Types)`


Create a new metric within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset to add the metric to.
- **metric** (`Metric`): The metric object containing the configuration and metadata.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the create operation.

##### `update_metric(self, dataset_id: UUID, metric: Metric) -> [MaxMutationResponse](API-Types)`


Update an existing metric within a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the metric.
- **metric** (`Metric`): The metric object containing the updated configuration and metadata.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the update operation.

##### `delete_metric(self, dataset_id: UUID, metric_id: str) -> [MaxMutationResponse](API-Types)`


Delete a metric from a dataset.


**Parameters:**

- **dataset_id** (`UUID`): The UUID of the dataset containing the metric.
- **metric_id** (`str`): The ID of the metric to delete.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the delete operation.

##### `create_database_kshot(self, database_kshot: dict[(str, Any)]) -> CreateDatabaseKShotResponse`


Create a new database k-shot.


**Parameters:**

- **database_kshot** (`Dict`): The database k-shot dictionary containing all necessary metadata and configuration. Must follow the DatabaseKShot type definition with fields: - databaseId: UUID (required) - question: str (required) - renderedPrompt: str (optional) - explanation: str (optional) - sql: str (optional) - title: str (optional) - visualization: JSON (optional) - isActive: bool (optional)


**Returns:**

`CreateDatabaseKShotResponse` - The result of the GraphQL mutation containing the created k-shot details.

##### `delete_database_kshot(self, database_kshot_id: UUID) -> [MaxMutationResponse](API-Types)`


Delete a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The UUID of the database k-shot to delete.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the delete operation.

##### `update_database_kshot_question(self, database_kshot_id: UUID, question: str) -> [MaxMutationResponse](API-Types)`


Update the question of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **question** (`str`): The new question to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated question.

##### `update_database_kshot_rendered_prompt(self, database_kshot_id: UUID, rendered_prompt: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the rendered prompt of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **rendered_prompt** (`Optional[str]`, optional): The new rendered prompt to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated rendered prompt.

##### `update_database_kshot_explanation(self, database_kshot_id: UUID, explanation: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the explanation of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **explanation** (`Optional[str]`, optional): The new explanation to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated explanation.

##### `update_database_kshot_sql(self, database_kshot_id: UUID, sql: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the SQL of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **sql** (`Optional[str]`, optional): The new SQL to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated SQL.

##### `update_database_kshot_title(self, database_kshot_id: UUID, title: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the title of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **title** (`Optional[str]`, optional): The new title to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated title.

##### `update_database_kshot_visualization(self, database_kshot_id: UUID, visualization: Optional[Dict]) -> [MaxMutationResponse](API-Types)`


Update the visualization of a database k-shot.


**Parameters:**

- **database_kshot_id** (`UUID`): The unique identifier of the database k-shot to be updated.
- **visualization** (`Optional[Dict]`, optional): The new visualization JSON to assign to the database k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated visualization.

##### `get_dataset_kshots(self, dataset_id: UUID, search_input: Optional[DatasetKShotSearchInput], paging: Optional[PagingInput]) -> PagedDatasetKShots`


Retrieve dataset k-shots based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **dataset_id** (`UUID`): The dataset_id that contains the k-shots
- **search_input** (`DatasetKShotSearchInput`, optional): An object specifying the search criteria for the k-shots. If None, no filters are applied
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`PagedDatasetKShots` - A paged collection of dataset k-shots. Returns an empty `PagedDatasetKShots` instance if an error occurs during retrieval.

##### `get_dataset_kshot_by_id(self, dataset_kshot_id: UUID) -> Optional[DatasetKShot]`


Retrieve a dataset k-shot by its ID.

This method queries the backend for a dataset k-shot using the given unique identifier.
If the k-shot is found, it is returned as a `DatasetKShot` object. If not found or
if an error occurs during the query, `None` is returned.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to retrieve.


**Returns:**

`DatasetKShot or None` - The dataset k-shot object if found, or `None` if not found or if an error occurs.

##### `create_dataset_kshot(self, dataset_kshot: dict[(str, Any)]) -> CreateDatasetKShotResponse`


Create a new dataset k-shot.


**Parameters:**

- **dataset_kshot** (`Dict`): The dataset k-shot dictionary containing all necessary metadata and configuration. Must follow the DatasetKShot type definition with fields: - datasetId: UUID (required) - question: str (required) - renderedPrompt: str (optional) - explanation: str (optional) - sql: str (optional) - title: str (optional) - visualization: JSON (optional) - isActive: bool (optional)


**Returns:**

`CreateDatasetKShotResponse` - The result of the GraphQL mutation containing the created k-shot details.

##### `delete_dataset_kshot(self, dataset_kshot_id: UUID) -> [MaxMutationResponse](API-Types)`


Delete a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be deleted.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the deletion details.

##### `update_dataset_kshot_question(self, dataset_kshot_id: UUID, question: str) -> [MaxMutationResponse](API-Types)`


Update the question of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **question** (`str`): The new question to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated question.

##### `update_dataset_kshot_rendered_prompt(self, dataset_kshot_id: UUID, rendered_prompt: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the rendered prompt of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **rendered_prompt** (`Optional[str]`, optional): The new rendered prompt to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated rendered prompt.

##### `update_dataset_kshot_explanation(self, dataset_kshot_id: UUID, explanation: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the explanation of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **explanation** (`Optional[str]`, optional): The new explanation to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated explanation.

##### `update_dataset_kshot_sql(self, dataset_kshot_id: UUID, sql: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the SQL of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **sql** (`Optional[str]`, optional): The new SQL to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated SQL.

##### `update_dataset_kshot_title(self, dataset_kshot_id: UUID, title: Optional[str]) -> [MaxMutationResponse](API-Types)`


Update the title of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **title** (`Optional[str]`, optional): The new title to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated title.

##### `update_dataset_kshot_visualization(self, dataset_kshot_id: UUID, visualization: Optional[Dict]) -> [MaxMutationResponse](API-Types)`


Update the visualization of a dataset k-shot.


**Parameters:**

- **dataset_kshot_id** (`UUID`): The unique identifier of the dataset k-shot to be updated.
- **visualization** (`Optional[Dict]`, optional): The new visualization JSON to assign to the dataset k-shot.


**Returns:**

`[MaxMutationResponse](API-Types)` - The result of the GraphQL mutation containing the updated visualization.

## Functions

### `create_df_from_data(data: Dict[(str, any)])`


Create a pandas DataFrame from structured data dictionary.


**Parameters:**

- **data** (`Dict[str, any]`): A dictionary containing 'columns' and optionally 'rows' keys. The 'columns' key should contain a list of column dictionaries with 'name' keys. The 'rows' key should contain a list of row dictionaries with 'data' keys.


**Returns:**

`DataFrame` - A pandas DataFrame created from the input data. Returns an empty DataFrame with the same columns if the only row contains all NaN values.
