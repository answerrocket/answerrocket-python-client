# answer_rocket.skill

## Classes

### `RunSkillResult`

Result object for synchronous skill execution.


**Attributes:**

- **data** (`[ChatReportOutput](API-Types) | None`): The output data from the skill execution.

#### Methods

##### `__init__(self, success: bool)`

### `AsyncSkillRunResult`

Result object for asynchronous skill execution.


**Attributes:**

- **execution_id** (`str | None`): The unique execution ID for tracking the async skill run.

#### Methods

##### `__init__(self, success: bool)`

### `Skill`

Provides tools to interact with copilot skills directly.

#### Methods

##### `__init__(self, config: [ClientConfig](API-Types), gql_client: GraphQlClient)`


Initialize the Skill client.


**Parameters:**

- **config** (`[ClientConfig](API-Types)`): The client configuration.
- **gql_client** (`GraphQlClient`): The GraphQL client for API communication.

##### `run(self, copilot_id: str, skill_name: str, parameters: dict | None, validate_parameters: bool) -> [RunSkillResult](API-Types)`


Run a skill synchronously and return its full output.

Does not stream intermediate skill output.


**Parameters:**

- **copilot_id** (`str`): The ID of the copilot to run the skill on.
- **skill_name** (`str`): The name of the skill to execute.
- **parameters** (`dict | None`, optional): Dictionary of parameters to pass to the skill.
- **validate_parameters** (`bool`, optional): Whether to apply guardrails to parameters before execution. Defaults to False.


**Returns:**

`[RunSkillResult](API-Types)` - The full output object of the skill execution.

##### `run_async(self, copilot_id: str, skill_name: str, parameters: dict | None) -> [AsyncSkillRunResult](API-Types)`


Start a skill execution asynchronously and return an execution ID immediately.


**Parameters:**

- **copilot_id** (`str`): The ID of the copilot to run the skill on.
- **skill_name** (`str`): The name of the skill to execute.
- **parameters** (`dict | None`, optional): Dictionary of parameters to pass to the skill.


**Returns:**

`[AsyncSkillRunResult](API-Types)` - Result containing execution_id if successful.

##### `get_async_status(self, execution_id: str) -> AsyncSkillStatusResponse`


Get the status and result of an async skill execution.


**Parameters:**

- **execution_id** (`str`): The execution ID returned from run_async.


**Returns:**

`AsyncSkillStatusResponse` - Result with status and data if completed, None if error occurs.

##### `update_loading_message(self, message: str)`


Update the loading message for the current skill execution.


**Parameters:**

- **message** (`str`): The loading message to display to the user.
