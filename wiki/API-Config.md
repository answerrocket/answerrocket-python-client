# answer_rocket.config

## Classes

### `Config`

Helper for accessing config, whether local or fetched from the configured server.

#### Methods

##### `__init__(self, config: [[API-Types#clientconfig|ClientConfig]], gql_client: GraphQlClient) -> None`


Initialize the Config helper.


**Parameters:**

- **config** (`[[API-Types#clientconfig|ClientConfig]]`): The client configuration containing copilot and connection details.
- **gql_client** (`GraphQlClient`): The GraphQL client for making server requests.

##### `get_artifact(self, artifact_path: str) -> str`


artifact path: this is the filepath to your artifact relative to the root of your project.
Server-side overrides are keyed on this path and will be fetched first when running inside AnswerRocket

##### `get_copilots(self) -> list[MaxCopilot]`


Retrieve all copilots available to the user with their metadata.


**Returns:**

`list[MaxCopilot]` - A list of MaxCopilot objects.

##### `get_copilot(self, use_published_version: bool, copilot_id: str) -> MaxCopilot`


Retrieve information about a specific copilot.


**Parameters:**

- **use_published_version** (`bool`, optional): Whether to use the published version. Defaults to True.
- **copilot_id** (`str`, optional): The ID of the copilot. If None, uses the configured copilot ID.


**Returns:**

`MaxCopilot | None` - The copilot information, or None if an error occurs.

##### `get_copilot_skill(self, use_published_version: bool, copilot_id: str, copilot_skill_id: str) -> MaxCopilotSkill`


Retrieve information about a specific copilot skill.


**Parameters:**

- **use_published_version** (`bool`, optional): Whether to use the published version. Defaults to True.
- **copilot_id** (`str`, optional): The ID of the copilot. If None, uses the configured copilot ID.
- **copilot_skill_id** (`str`, optional): The ID of the copilot skill. If None, uses the configured skill ID.


**Returns:**

`MaxCopilotSkill | None` - The copilot skill information, or None if an error occurs.

##### `get_copilot_hydrated_reports(self, copilot_id: Optional[str], override_dataset_id: Optional[str], load_all_skills: bool) -> [HydratedReport]`


Get hydrated reports for a copilot.


**Parameters:**

- **copilot_id** (`str`, optional): The copilot ID. Defaults to the configured copilot_id.
- **override_dataset_id** (`str`, optional): Optional dataset ID to override the copilot's default dataset.
- **load_all_skills** (`bool`, optional): Whether to load all skills or just active ones. Defaults to False.


**Returns:**

`list[HydratedReport] | None` - List of hydrated report objects, or None if an error occurs.

##### `create_copilot_question(self, nl: str, skill_id: UUID, hint: str, parameters) -> MaxCreateCopilotQuestionResponse`


Create a new copilot question.


**Parameters:**

- **nl** (`str`): The natural language question.
- **skill_id** (`UUID`, optional): The ID of the skill to associate with the question.
- **hint** (`str`, optional): A hint for the question.
- **parameters** (`Any`, optional): Additional parameters for the question.


**Returns:**

`MaxCreateCopilotQuestionResponse | None` - The response containing the created question, or None if an error occurs.

##### `update_copilot_question(self, copilot_question_id: UUID, nl: str, skill_id: UUID, hint: str, parameters) -> [[API-Types#maxmutationresponse|MaxMutationResponse]]`


Update an existing copilot question.


**Parameters:**

- **copilot_question_id** (`UUID`): The ID of the question to update.
- **nl** (`str`, optional): The updated natural language question.
- **skill_id** (`UUID`, optional): The updated skill ID.
- **hint** (`str`, optional): The updated hint.
- **parameters** (`Any`, optional): The updated parameters.


**Returns:**

`[[API-Types#maxmutationresponse|MaxMutationResponse]] | None` - The mutation response, or None if an error occurs.

##### `delete_copilot_chat_question(self, copilot_question_id: UUID) -> [[API-Types#maxmutationresponse|MaxMutationResponse]]`


Delete a copilot question.


**Parameters:**

- **copilot_question_id** (`UUID`): The ID of the question to delete.


**Returns:**

`[[API-Types#maxmutationresponse|MaxMutationResponse]] | None` - The mutation response, or None if an error occurs.

##### `get_current_user(self) -> MaxUser`


Retrieve information about the current authenticated user.


**Returns:**

`MaxUser | None` - The current user information, or None if an error occurs.

##### `get_prompt(self, llm_prompt_id: UUID, template_vars: Dict[(str, Any)], k_shot_match: str) -> MaxLLmPrompt`


Retrieve an LLM prompt with template variables and k-shot matching.


**Parameters:**

- **llm_prompt_id** (`UUID`): The ID of the LLM prompt to retrieve.
- **template_vars** (`Dict[str, Any]`): Template variables to substitute in the prompt.
- **k_shot_match** (`str`): The k-shot matching criteria.


**Returns:**

`MaxLLmPrompt | None` - The LLM prompt with substitutions applied, or None if an error occurs.

##### `clear_copilot_cache(self, copilot_id: UUID) -> [[API-Types#maxmutationresponse|MaxMutationResponse]]`


Clear the cache for a copilot.


**Parameters:**

- **copilot_id** (`UUID`, optional): The ID of the copilot to clear cache for. If None, uses the configured copilot ID.


**Returns:**

`[[API-Types#maxmutationresponse|MaxMutationResponse]]` - The response from the clear cache operation, or None if an error occurs.

## Functions
