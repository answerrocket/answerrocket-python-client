# answer_rocket.llm

## Classes

### `LlmChatMessage`

A chat message for passing to an LLM API.


**Attributes:**

- **role** (`str`): The role of the participant in this chat.
- **content** (`str`): The chat message.

### `LlmFunctionProperty`

Property definition for LLM function parameters.


**Attributes:**

- **type** (`str`): The data type of the property.
- **description** (`str`): Description of what the property represents.

### `LlmFunctionParameters`

Parameters definition for an LLM function.


**Attributes:**

- **type** (`str`): The type of parameters (typically 'object').
- **properties** (`dict[str, [[API-Types|LlmFunctionProperty]]]`): Dictionary of property definitions.
- **required** (`list[str]`): List of required property names.

### `LlmFunction`

Function definition for LLM tool calling.


**Attributes:**

- **name** (`str`): The name of the function.
- **description** (`str`): Description of what the function does.
- **parameters** (`[[API-Types|LlmFunctionParameters]]`): Parameter definitions for the function.

### `Llm`

Client for interacting with LLM APIs through AnswerRocket.

#### Methods

##### `__init__(self, config: [[API-Types|ClientConfig]], gql_client)`


Initialize the LLM client.


**Parameters:**

- **config** (`[[API-Types|ClientConfig]]`): The client configuration.
- **gql_client** (`GraphQlClient`): The GraphQL client for API communication.

##### `chat_completion(self, messages: list[[[API-Types|LlmChatMessage]]], model_override: str | None, functions: list[[[API-Types|LlmFunction]]] | None)`


Call an LLM API's chat completion endpoint with the provided messages.


**Parameters:**

- **messages** (`list[[[API-Types|LlmChatMessage]]]`): List of chat messages with role and content.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.
- **functions** (`list[[[API-Types|LlmFunction]]] | None`, optional): Available functions/tools to send to the language model.


**Returns:**

`dict` - The raw response from the model API.

##### `chat_completion_with_prompt(self, prompt_name: str, prompt_variables: dict, model_override: str | None, functions: list[[[API-Types|LlmFunction]]] | None)`


Call an LLM API's chat completion endpoint with a named prompt.


**Parameters:**

- **prompt_name** (`str`): The name of the prompt to use.
- **prompt_variables** (`dict`): Dictionary of variables to pass to the prompt.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.
- **functions** (`list[[[API-Types|LlmFunction]]] | None`, optional): Available functions/tools to send to the language model.


**Returns:**

`dict` - The raw response from the model API.

##### `narrative_completion(self, prompt: str, model_override: str | None)`


Call an LLM API's completion endpoint with the provided prompt.


**Parameters:**

- **prompt** (`str`): The prompt to send to the model.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.


**Returns:**

`dict` - The raw response from the model API.

##### `narrative_completion_with_prompt(self, prompt_name: str, prompt_variables: dict, model_override: str | None)`


Call an LLM API's completion endpoint with a named prompt.


**Parameters:**

- **prompt_name** (`str`): The name of the prompt to use.
- **prompt_variables** (`dict`): Dictionary of variables to pass to the prompt.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.


**Returns:**

`dict` - The raw response from the model API.

##### `sql_completion(self, messages: list[[[API-Types|LlmChatMessage]]], model_override: str | None, functions: list[[[API-Types|LlmFunction]]] | None)`


Call an LLM API's chat completion endpoint using the SQL model.

Uses the environment's configured 'SQL' model for SQL-specific tasks.


**Parameters:**

- **messages** (`list[[[API-Types|LlmChatMessage]]]`): List of chat messages with role and content.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.
- **functions** (`list[[[API-Types|LlmFunction]]] | None`, optional): Available functions/tools to send to the language model.


**Returns:**

`dict` - The raw response from the model API.

##### `research_completion(self, messages: list[[[API-Types|LlmChatMessage]]], model_override: str | None, functions: list[[[API-Types|LlmFunction]]] | None)`


Call an LLM API's chat completion endpoint using the Research model.

Uses the environment's configured 'Research' model for research tasks.


**Parameters:**

- **messages** (`list[[[API-Types|LlmChatMessage]]]`): List of chat messages with role and content.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.
- **functions** (`list[[[API-Types|LlmFunction]]] | None`, optional): Available functions/tools to send to the language model.


**Returns:**

`dict` - The raw response from the model API.

##### `research_completion_with_prompt(self, prompt_name: str, prompt_variables: dict, model_override: str | None, functions: list[[[API-Types|LlmFunction]]] | None)`


Call an LLM API's chat completion endpoint with a named prompt using the Research model.

Uses the environment's configured 'Research' model for research tasks.


**Parameters:**

- **prompt_name** (`str`): The name of the prompt to use.
- **prompt_variables** (`dict`): Dictionary of variables to pass to the prompt.
- **model_override** (`str | None`, optional): Model name or ID to use instead of configured default.
- **functions** (`list[[[API-Types|LlmFunction]]] | None`, optional): Available functions/tools to send to the language model.


**Returns:**

`dict` - The raw response from the model API.
