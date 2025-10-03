# answer_rocket.chat

## Classes

### `Chat`

#### Methods

##### `__init__(self, gql_client: GraphQlClient, config: [[API-Types#clientconfig|ClientConfig]])`

##### `ask_question(self, copilot_id: str, question: str, thread_id: str, skip_report_cache: bool, dry_run_type: str, model_overrides: dict, indicated_skills: list[str], history: list[dict], question_type: [[API-Types#questiontype|QuestionType]], thread_type: [[API-Types#threadtype|ThreadType]]) -> [[API-Types#maxchatentry|MaxChatEntry]]`


Calls the Max chat pipeline to answer a natural language question and receive analysis and insights
in response.


**Parameters:**

- **copilot_id** (`str`): The ID of the copilot to run the question against.
- **question** (`str`): The natural language question to ask the engine.
- **thread_id** (`str`, optional): ID of the thread/conversation to run the question on. The question and answer will be added to the bottom of the thread.
- **skip_report_cache** (`bool`, optional): Should the report cache be skipped for this question? Defaults to False.
- **dry_run_type** (`str`, optional): If provided, run a dry run at the specified level: 'SKIP_SKILL_EXEC', 'SKIP_SKILL_NLG'.
- **model_overrides** (`dict`, optional): A dictionary of model types to model names to override the LLM model used. Model type options are 'CHAT', 'EMBEDDINGS', 'NARRATIVE'.
- **indicated_skills** (`list[str]`, optional): A list of skill names that the copilot will be limited to choosing from. If only 1 skill is provided the copilot will be guaranteed to execute that skill.
- **history** (`list[dict]`, optional): A list of messages to be used as the conversation history for the question.
- **question_type** (`[[API-Types#questiontype|QuestionType]]`, optional): The type of question being asked. This is used to categorize the question and can determine how the UI chooses to display it.
- **thread_type** (`[[API-Types#threadtype|ThreadType]]`, optional): The type of thread being created. This is used to categorize the thread and can determine how the UI chooses to display it.


**Returns:**

`[[API-Types#maxchatentry|MaxChatEntry]]` - The ChatEntry response object associated with the answer from the pipeline.

##### `add_feedback(self, entry_id: str, feedback_type: [[API-Types#feedbacktype|FeedbackType]], feedback_text: str) -> bool`


This adds feedback to a chat entry.


**Parameters:**

- **entry_id** (`str`): The id of the chat entry.
- **feedback_type** (`[[API-Types#feedbacktype|FeedbackType]]`): The type of feedback to add.
- **feedback_text** (`str`, optional): The text of the feedback.


**Returns:**

`bool` - True if the feedback was added successfully, False otherwise.

##### `get_threads(self, copilot_id: str, start_date: datetime, end_date: datetime) -> list[[[API-Types#maxchatthread|MaxChatThread]]]`


Fetches all threads for a given copilot and date range.


**Parameters:**

- **copilot_id** (`str`): The ID of the copilot to fetch threads for.
- **start_date** (`datetime`, optional): The start date of the range to fetch threads for.
- **end_date** (`datetime`, optional): The end date of the range to fetch threads for.


**Returns:**

`list[[[API-Types#maxchatthread|MaxChatThread]]]` - A list of ChatThread objects.

##### `get_entries(self, thread_id: str, offset: int, limit: int) -> list[[[API-Types#maxchatentry|MaxChatEntry]]]`


Fetches all entries for a given thread.


**Parameters:**

- **thread_id** (`str`): The ID of the thread to fetch entries for.
- **offset** (`int`, optional): The offset to start fetching entries from.
- **limit** (`int`, optional): The maximum number of entries to fetch.


**Returns:**

`list[[[API-Types#maxchatentry|MaxChatEntry]]]` - A list of ChatEntry objects.

##### `evaluate_entry(self, entry_id: str, evals: list[str]) -> [[API-Types#evaluatechatquestionresponse|EvaluateChatQuestionResponse]]`


Runs and fetches the inputted evaluations for a given entry.


**Parameters:**

- **entry_id** (`str`): The ID of the entry to fetch evaluation for.
- **evals** (`list[str]`): A list of strings containing the evaluations to run on the entry.


**Returns:**

`[[API-Types#evaluatechatquestionresponse|EvaluateChatQuestionResponse]]` - The evaluation response object containing evaluation results.

##### `share_chat_thread(self, original_thread_id: str) -> [[API-Types#sharedthread|SharedThread]]`


Share a chat thread by its ID.


**Parameters:**

- **original_thread_id** (`str`): The ID of the original thread to share.


**Returns:**

`[[API-Types#sharedthread|SharedThread]]` - The shared thread object.

##### `get_chat_entry(self, entry_id: str) -> [[API-Types#maxchatentry|MaxChatEntry]]`


Retrieve a chat entry by its ID.


**Parameters:**

- **entry_id** (`str`): The ID of the chat entry to retrieve.


**Returns:**

`[[API-Types#maxchatentry|MaxChatEntry]]` - The chat entry object.

##### `get_chat_thread(self, thread_id: str) -> [[API-Types#maxchatthread|MaxChatThread]]`


Retrieve a chat thread by its ID.


**Parameters:**

- **thread_id** (`str`): The ID of the chat thread to retrieve.


**Returns:**

`[[API-Types#maxchatthread|MaxChatThread]]` - The chat thread object.

##### `create_new_thread(self, copilot_id: str, thread_type: [[API-Types#threadtype|ThreadType]]) -> [[API-Types#maxchatthread|MaxChatThread]]`


Create a new chat thread for the specified agent.


**Parameters:**

- **copilot_id** (`str`): The ID of the agent to create the thread for.
- **thread_type** (`[[API-Types#threadtype|ThreadType]]`, optional): The type of thread to create. Defaults to CHAT. For most purposes CHAT is the only type needed.


**Returns:**

`[[API-Types#maxchatthread|MaxChatThread]]` - The newly created chat thread object.

##### `queue_chat_question(self, question: str, thread_id: str, skip_cache: bool, model_overrides: dict, indicated_skills: list[str], history: list[dict]) -> [[API-Types#maxchatentry|MaxChatEntry]]`


This queues up a question for processing. Unlike ask_question, this will not wait for the processing to
complete. It will immediately return a shell entry with an id you can use to query for the results.


**Parameters:**

- **question** (`str`): The text of the user's question.
- **thread_id** (`str`): ID of the thread the question is being sent to.
- **skip_cache** (`bool`, optional): Set to true to force a fresh run of the question, ignoring any existing skill result caches. Defaults to False.
- **model_overrides** (`dict`, optional): A dictionary of model types to model names to override the LLM model used. Model type options are 'CHAT', 'EMBEDDINGS', 'NARRATIVE'.
- **indicated_skills** (`list[str]`, optional): A list of skill names that the copilot will be limited to choosing from. If only 1 skill is provided the copilot will be guaranteed to execute that skill.
- **history** (`list[dict]`, optional): A list of messages to be used as the conversation history for the question.


**Returns:**

`[[API-Types#maxchatentry|MaxChatEntry]]` - A shell entry with an id you can use to query for the results.

##### `cancel_chat_question(self, entry_id: str) -> [[API-Types#maxchatentry|MaxChatEntry]]`


This deletes the entry from its thread and attempts to abandon the question's processing if it is still ongoing.


**Parameters:**

- **entry_id** (`str`): The id of the chat entry.


**Returns:**

`[[API-Types#maxchatentry|MaxChatEntry]]` - The deleted entry.

##### `get_user(self, user_id: str) -> [[API-Types#maxchatuser|MaxChatUser]]`


This fetches a user by their ID.


**Parameters:**

- **user_id** (`str`): The id of the user.


**Returns:**

`[[API-Types#maxchatuser|MaxChatUser]]` - A [[API-Types#maxchatuser|MaxChatUser]] object.

##### `get_all_chat_entries(self, offset, limit, filters) -> list[[[API-Types#maxchatentry|MaxChatEntry]]]`


Fetches all chat entries with optional filters.


**Parameters:**

- **offset** (`int`, optional): The offset to start fetching entries from. Defaults to 0.
- **limit** (`int`, optional): The maximum number of entries to fetch. Defaults to 100.
- **filters** (`dict`, optional): A dictionary of filters to apply to the query. Supports all filtering available in the query browser.


**Returns:**

`list[[[API-Types#maxchatentry|MaxChatEntry]]]` - A list of ChatEntry objects.

##### `get_skill_memory_payload(self, chat_entry_id: str) -> dict`


Fetches the skill memory payload for a given chat entry.


**Parameters:**

- **chat_entry_id** (`str`): The id of the chat entry.


**Returns:**

`dict` - The skill memory payload for the given chat entry.

##### `set_skill_memory_payload(self, skill_memory_payload: dict, chat_entry_id: str) -> bool`


Sets the skill memory payload for a given chat entry.


**Parameters:**

- **skill_memory_payload** (`dict`): The skill memory payload to set -- must be JSON serializable.
- **chat_entry_id** (`str`, optional): The id of the chat entry.


**Returns:**

`bool` - True if the skill memory payload was set successfully, False otherwise.

##### `get_dataframes_for_entry(self, entry_id: str) -> [pd.DataFrame]`


This fetches the dataframes (with metadata) for a given chat entry.


**Parameters:**

- **entry_id** (`str`): The answer entry to fetch dataframes for.


**Returns:**

`list[pd.DataFrame]` - A list of dataframes and metadata for the given chat entry.

##### `get_chat_artifact(self, chat_artifact_id: UUID) -> Optional[[[API-Types#chatartifact|ChatArtifact]]]`


Retrieve a chat artifact by its ID.

This method queries the backend for a chat artifact using the given unique identifier.
If the artifact is found, it is returned as a `ChatArtifact` object. If not found or
if an error occurs during the query, `None` is returned.


**Parameters:**

- **chat_artifact_id** (`UUID`): The unique identifier of the chat artifact to retrieve.


**Returns:**

`[[API-Types#chatartifact|ChatArtifact]] or None` - The chat artifact object if found, or `None` if not found or if an error occurs.

##### `get_chat_artifacts(self, search_input: Optional[ChatArtifactSearchInput], paging: Optional[PagingInput]) -> [[API-Types#pagedchatartifacts|PagedChatArtifacts]]`


Retrieve paged chat artifacts based on optional search and paging criteria.

If no `search_input` or `paging` is provided, default values will be used.


**Parameters:**

- **search_input** (`ChatArtifactSearchInput`, optional): An object specifying the search criteria for chat artifacts. If None, no filters are applied on name or misc_info.
- **paging** (`PagingInput`, optional): An object specifying pagination details such as page number and page size. If None, defaults to page 1 with a page size of 100.


**Returns:**

`[[API-Types#pagedchatartifacts|PagedChatArtifacts]]` - A paged collection of chat artifacts. Returns an empty `[[API-Types#pagedchatartifacts|PagedChatArtifacts]]` instance if an error occurs during retrieval.

##### `create_chat_artifact(self, chat_artifact: [[API-Types#chatartifact|ChatArtifact]]) -> [[API-Types#maxmutationresponse|MaxMutationResponse]]`


Submits a GraphQL mutation to create a new chat artifact.


**Parameters:**

- **chat_artifact** (`[[API-Types#chatartifact|ChatArtifact]]`): The chat artifact object containing the data to be created.


**Returns:**

`[[API-Types#maxmutationresponse|MaxMutationResponse]]` - The response object containing the result of the mutation, specifically the created chat artifact.

##### `delete_chat_artifact(self, chat_artifact_id: uuid) -> [[API-Types#maxmutationresponse|MaxMutationResponse]]`


Submits a GraphQL mutation to delete an existing chat artifact by its ID.


**Parameters:**

- **chat_artifact_id** (`uuid`): The UUID of the chat artifact to delete.


**Returns:**

`[[API-Types#maxmutationresponse|MaxMutationResponse]]` - The response object containing the result of the deletion mutation.
