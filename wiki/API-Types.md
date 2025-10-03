# answer_rocket.types

Type definitions, result classes, and constants used throughout the AnswerRocket SDK.

## Constants

- **RESULT_EXCEPTION_CODE** = `1000` (from `types`)



## Type Aliases

### `FeedbackType`

*Defined in `answer_rocket.chat`*


```python
FeedbackType = Literal[('CHAT_POSITIVE', 'CHAT_NEGATIVE')]
```


### `QuestionType`

*Defined in `answer_rocket.chat`*


```python
QuestionType = Literal[('DRILLDOWN', 'EXAMPLE', 'FOLLOWUP', 'RESEARCHER_REPORT', 'SAVED', 'SCHEDULED', 'SHARED', 'SKILL_PREVIEW', 'TEST_RUN', 'USER_WRITTEN', 'XML_CALLBACK')]
```


### `ThreadType`

*Defined in `answer_rocket.chat`*


```python
ThreadType = Literal[('CHAT', 'COPILOT_QUESTION_PREVIEW', 'RESEARCH', 'SHARED', 'SKILL', 'TEST')]
```


## Type Classes

### `MaxResult`

*Defined in `answer_rocket.types`*


Base result class for AnswerRocket API operations.


**Attributes:**

- **success** (`bool`): Whether the operation succeeded. Defaults to False.
- **code** (`int | str | None`): Error code or status code from the operation.
- **error** (`str | None`): Error message if the operation failed.

### `ExecuteSqlQueryResult`

*Defined in `answer_rocket.data`*


Result object for SQL query execution operations.


**Attributes:**

- **df** (`DataFrame | None`): The result of the SQL query as a pandas DataFrame.
- **data** (`deprecated`): Deprecated field. Use df instead for DataFrame results.

### `DomainObjectResult`

*Defined in `answer_rocket.data`*


Result object for domain object retrieval operations.

### `RunMaxSqlGenResult`

*Defined in `answer_rocket.data`*


Result object for Max SQL generation operations.


**Attributes:**

- **sql** (`str | None`): The generated SQL query string.
- **df** (`DataFrame | None`): The result of executing the generated SQL as a pandas DataFrame.
- **row_limit** (`int | None`): The row limit applied to the SQL query.
- **data** (`deprecated`): Deprecated field. Use df instead for DataFrame results.

### `RunSqlAiResult`

*Defined in `answer_rocket.data`*


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
- **prior_runs** (`List[[RunSqlAiResult](API-Types.md#runsqlairesult)]`): List of prior runs for comparison or iteration tracking.

### `RunSkillResult`

*Defined in `answer_rocket.skill`*


Result object for synchronous skill execution.


**Attributes:**

- **data** (`[ChatReportOutput](API-Types.md#chatreportoutput) | None`): The output data from the skill execution.

### `AsyncSkillRunResult`

*Defined in `answer_rocket.skill`*


Result object for asynchronous skill execution.


**Attributes:**

- **execution_id** (`str | None`): The unique execution ID for tracking the async skill run.

### `ChatLoadingInfo`

*Defined in `answer_rocket.output`*


Describes the loading state of an object in chat.


**Attributes:**

- **message** (`str`): User-friendly message to describe the current loading step.

### `ContentBlock`

*Defined in `answer_rocket.output`*


Represents a block of content that is produced by a skill and displayed to the user.

Blocks contain metadata as well as their final XML payload.


**Attributes:**

- **id** (`str`): Unique ID for the block.
- **title** (`str | None`): The user-friendly name of the block that will be displayed on the frontend.
- **loading_info** (`[ChatLoadingInfo](API-Types.md#chatloadinginfo) | None`): Details around the block's current loading state.
- **payload** (`str | None`): XML payload for the block to display, represented as a string.
- **is_collapsible** (`bool | None`): Whether or not the block can be collapsed by the user.
- **layout_json** (`str | None`): An alternative to payload, this is a JSON representation of the block's visual layout.

### `ChatReportOutput`

*Defined in `answer_rocket.output`*


Contains all the possible information a report can return to the chat pipeline.


**Attributes:**

- **payload** (`str | None`): The complete XML string for the entire report.
- **content_blocks** (`List[[ContentBlock](API-Types.md#contentblock)]`): List of content blocks to display.
- **suggestions** (`List[str]`): List of suggested follow-up questions.
- **interpretation_notes** (`List[str]`): List of notes about how the query was interpreted.
- **final_message** (`str`): Final message to display to the user.
- **info** (`Any | None`): Any additional information the skill wants to include, typically for debugging.

### `LlmChatMessage`

*Defined in `answer_rocket.llm`*


A chat message for passing to an LLM API.


**Attributes:**

- **role** (`str`): The role of the participant in this chat.
- **content** (`str`): The chat message.

### `LlmFunctionProperty`

*Defined in `answer_rocket.llm`*


Property definition for LLM function parameters.


**Attributes:**

- **type** (`str`): The data type of the property.
- **description** (`str`): Description of what the property represents.

### `LlmFunctionParameters`

*Defined in `answer_rocket.llm`*


Parameters definition for an LLM function.


**Attributes:**

- **type** (`str`): The type of parameters (typically 'object').
- **properties** (`dict[str, [LlmFunctionProperty](API-Types.md#llmfunctionproperty)]`): Dictionary of property definitions.
- **required** (`list[str]`): List of required property names.

### `LlmFunction`

*Defined in `answer_rocket.llm`*


Function definition for LLM tool calling.


**Attributes:**

- **name** (`str`): The name of the function.
- **description** (`str`): Description of what the function does.
- **parameters** (`[LlmFunctionParameters](API-Types.md#llmfunctionparameters)`): Parameter definitions for the function.

### `ClientConfig`

*Defined in `answer_rocket.client_config`*


Configuration object for AnswerRocket client initialization.


**Attributes:**

- **url** (`str`): Environment URL.
- **token** (`str | None`): Authentication token.
- **tenant** (`str | None`): Tenant ID, provided automatically.
- **is_live_run** (`bool`): Set when the client is used in a skill run (as opposed to running locally).
- **answer_id** (`str | None`): The skill run answer_id that any answer-updating calls will use.
- **entry_answer_id** (`str | None`): The answer_id for the chat entry being created.
- **user_id** (`str | None`): Provided automatically or implicitly via the auth token.
- **copilot_id** (`str | None`): The copilot the skill is running within.
- **copilot_skill_id** (`str | None`): The id of the skill in the environment.
- **resource_base_path** (`str | None`): The base path to use for resources.
- **thread_id** (`str | None`): The thread ID for chat interactions.
- **chat_entry_id** (`str | None`): The chat entry ID for the current interaction.
