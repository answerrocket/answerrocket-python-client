# answer_rocket.output

## Classes

### `ChatLoadingInfo`

Describes the loading state of an object in chat.


**Attributes:**

- **message** (`str`): User-friendly message to describe the current loading step.

### `ContentBlock`

Represents a block of content that is produced by a skill and displayed to the user.

Blocks contain metadata as well as their final XML payload.


**Attributes:**

- **id** (`str`): Unique ID for the block.
- **title** (`str | None`): The user-friendly name of the block that will be displayed on the frontend.
- **loading_info** (`[[API-Types|ChatLoadingInfo]] | None`): Details around the block's current loading state.
- **payload** (`str | None`): XML payload for the block to display, represented as a string.
- **is_collapsible** (`bool | None`): Whether or not the block can be collapsed by the user.
- **layout_json** (`str | None`): An alternative to payload, this is a JSON representation of the block's visual layout.

### `ChatReportOutput`

Contains all the possible information a report can return to the chat pipeline.


**Attributes:**

- **payload** (`str | None`): The complete XML string for the entire report.
- **content_blocks** (`List[[[API-Types|ContentBlock]]]`): List of content blocks to display.
- **suggestions** (`List[str]`): List of suggested follow-up questions.
- **interpretation_notes** (`List[str]`): List of notes about how the query was interpreted.
- **final_message** (`str`): Final message to display to the user.
- **info** (`Any | None`): Any additional information the skill wants to include, typically for debugging.

### `OutputBuilder`

Builder for creating and managing chat report outputs.

Handles creating content blocks, updating their states, and managing the overall report output.

#### Methods

##### `__init__(self, config: [[API-Types|ClientConfig]], gql_client: GraphQlClient)`


Initialize the output builder.


**Parameters:**

- **config** (`[[API-Types|ClientConfig]]`): The client configuration.
- **gql_client** (`GraphQlClient`): The GraphQL client for API communication.

##### `add_block(self, title: str, loading_status: [[API-Types|ChatLoadingInfo]], xml: str, is_collapsible: bool, layout_json: str) -> str`


Add a new content block to the report output.

The newly added block becomes the default block for future updates until a new block is added.


**Parameters:**

- **title** (`str`, optional): The user-friendly name of the block displayed on the frontend.
- **loading_status** (`[[API-Types|ChatLoadingInfo]]`, optional): The loading state of the block.
- **xml** (`str`, optional): XML payload for the block to display.
- **is_collapsible** (`bool`, optional): Whether the block can be collapsed by the user. Defaults to True.
- **layout_json** (`str`, optional): Alternative to xml, JSON representation of the block's visual layout.


**Returns:**

`str` - The unique ID of the newly created block.

##### `remove_block(self, block_id: UUID) -> bool`


Remove the specified content block from the report output.

If no block_id is provided, the last block to be added will be removed.


**Parameters:**

- **block_id** (`UUID`, optional): The ID of the block to remove. If None, removes the last added block.


**Returns:**

`bool` - True if a block was removed, False otherwise.

##### `update_block(self, block_id: UUID, title: str, loading_info: [[API-Types|ChatLoadingInfo]], xml: str, is_collapsible: bool, layout_json: str) -> [[API-Types|ContentBlock]]`


Update the specified content block with provided parameters.

If no block_id is provided, the last block to be added will be updated.


**Parameters:**

- **block_id** (`UUID`, optional): The ID of the block to update. If None, updates the last added block.
- **title** (`str`, optional): The user-friendly name of the block displayed on the frontend.
- **loading_info** (`[[API-Types|ChatLoadingInfo]]`, optional): The loading state of the block.
- **xml** (`str`, optional): XML payload for the block to display.
- **is_collapsible** (`bool`, optional): Whether the block can be collapsed by the user.
- **layout_json** (`str`, optional): Alternative to xml, JSON representation of the block's visual layout.


**Returns:**

`[[API-Types|ContentBlock]]` - The updated content block.

##### `end_block(self, block_id: str) -> [[API-Types|ContentBlock]]`


Mark the specified content block as complete by removing its loading info.

If no block_id is provided, the last block to be added will be marked as complete.


**Parameters:**

- **block_id** (`str`, optional): The ID of the block to mark as complete. If None, marks the last added block.


**Returns:**

`[[API-Types|ContentBlock]]` - The updated content block.

##### `merge_output(self, changes: [[API-Types|ChatReportOutput]]) -> [[API-Types|ChatReportOutput]]`


Merge the provided changes into the current report output.


**Parameters:**

- **changes** (`[[API-Types|ChatReportOutput]]`): The changes to merge into the current output.


**Returns:**

`[[API-Types|ChatReportOutput]]` - The updated report output.
