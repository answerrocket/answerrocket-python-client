# answer_rocket.client

## Classes

### `AnswerRocketClient`

Main client for interacting with AnswerRocket services.

Provides access to data, configuration, chat, output building, skills, and LLM functionality.

#### Methods

##### `__init__(self, url: Optional[str], token: Optional[str], tenant: str)`


Initialize the AnswerRocket client.


**Parameters:**

- **url** (`str`, optional): The URL of your AnswerRocket instance. Can also be set via AR_URL environment variable.
- **token** (`str`, optional): A valid SDK token. Can also be set via AR_TOKEN environment variable.
- **tenant** (`str`, optional): The tenant identifier for multi-tenant deployments.

##### `can_connect(self) -> bool`


Check if the client can connect to and authenticate with the server.


**Returns:**

`bool` - True if connection and authentication succeed, False otherwise.
