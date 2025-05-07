import os
import uuid
from typing import Any, List

import sgqlc
from sgqlc.types import Arg, Variable
from typing_extensions import TypedDict

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import JSON, UUID as GQL_UUID, UUID


class ChatLoadingInfo(TypedDict):
    """
    Describes the loading state of an object in chat
    """
    message: str
    """
    User-friendly messaged to describe the current loading step
    """


class ContentBlock(TypedDict):
    """
    Represents a block of content that is produced by a skill and displayed to the user. Blocks contain metadata as
    well as their final XML payload.
    """
    id: str
    """
    Unique ID for the block
    """
    title: str | None
    """
    The user-friendly name of the block that will be displayed on the frontend
    """
    loading_info: ChatLoadingInfo | None
    """
    Details around the block's current loading state
    """
    payload: str | None
    """
    XML payload for the block to display, represented as a string.
    """
    is_collapsible: bool | None
    """
    Whether or not the block can be collapsed by the user
    """
    layout_json: str | None
    """
    An alternative to payload, this is a JSON representation of the block's visual layout
    """


class ChatReportOutput(TypedDict, total=False):
    """
    Contains all the possible information a report can return to the chat pipeline.
    """
    payload: str | None
    """
    The complete XML string for the entire report.
    """
    content_blocks: List[ContentBlock]
    suggestions: List[str]
    interpretation_notes: List[str]
    final_message: str
    info: Any | None
    """
    Any additional information the skill wants to include, typically to be used for debugging
    """


class OutputBuilder:

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient):
        self._gql_client = gql_client
        self._config = config
        self.answer_id = self._config.answer_id
        self.current_output = ChatReportOutput(
            payload=None,
            content_blocks=[],
            suggestions=[],
            interpretation_notes=[],
            final_message="",
            info=None
        )

    def _update_answer(self):
        if self.answer_id: # and self._config.is_live_run:
            query_args = {
                'answerId': self.answer_id,
                'payload': self.current_output,
                'entryAnswerId': self._config.entry_answer_id,
                'nudgeEntryId': self._config.chat_entry_id
            }
            query_vars = {
                'answer_id': Arg(sgqlc.types.non_null(GQL_UUID)),
                'payload': Arg(sgqlc.types.non_null(JSON)),
                'entry_answer_id': Arg(GQL_UUID),
                'nudge_entry_id': Arg(GQL_UUID)
            }

            operation = self._gql_client.mutation(variables=query_vars)

            update_mutation = operation.update_chat_answer_payload(
                answer_id=Variable('answer_id'),
                payload=Variable('payload'),
                entry_answer_id=Variable('entry_answer_id'),
                nudge_entry_id=Variable('nudge_entry_id'),
            )

            self._gql_client.submit(operation, query_args)

    def add_block(self, title: str = None, loading_status: ChatLoadingInfo = None, xml: str = None,
                  is_collapsible: bool = True, layout_json: str = None) -> str:
        """
        Adds a new content block to the report output. The newly added blocks becomes the default block for
        future updates until a new block is added.

        :param title: The user-friendly name of the block that will be displayed on the frontend
        :param loading_status: The loading state of the block
        :param xml: XML payload for the block to display, represented as a string.
        :param is_collapsible: Whether the block can be collapsed by the user
        :param layout_json: An alternative to xml, this is a JSON representation of the block's visual layout
        """
        new_block = ContentBlock(id=str(uuid.uuid4()), title=title, loading_info=loading_status, payload=xml,
                                 is_collapsible=is_collapsible, layout_json=layout_json)
        self.current_output["content_blocks"].append(new_block)
        self._update_answer()

        return new_block['id']

    def remove_block(self, block_id: UUID = None) -> bool:
        """
        Removes the specified content block from the report output. If no block_id is provided, the last block to be
        added will be removed.
        param block_id: The id of the block to remove, if none is provided the last block to be added will be removed
        """
        for b in self.current_output["content_blocks"]:
            if b['id'] == block_id:
                self.current_output["content_blocks"].remove(b)
                self._update_answer()
                return True
        return False


    def update_block(self, block_id: UUID = None, title: str = None, loading_info: ChatLoadingInfo = None,
                     xml: str = None, is_collapsible: bool = None, layout_json: str = None) -> ContentBlock:
        """
        Updates the specified content block with any or all of the provided parameters. If no block_id is provided,
        the last block to be added will be updated.

        :param block_id: The id of the block to update, if none is provided the last block to be added will be updated
        :param title: The user-friendly name of the block that will be displayed on the frontend, leave blank for no-update
        :param loading_info: The loading state of the block, leave blank for no-update
        :param xml: XML payload for the block to display, represented as a string, leave blank for no-update
        :param is_collapsible: Whether the block can be collapsed by the user, leave blank for no-update
        :param layout_json: An alternative to xml, this is a JSON representation of the block's visual layout
        """

        def get_updated_block(b: ContentBlock):
            if title:
                b['title'] = title
            if loading_info:
                b['loading_info'] = loading_info
            if xml:
                b['payload'] = xml
            if is_collapsible is not None:
                b['is_collapsible'] = is_collapsible
            if layout_json:
                b['layout_json'] = layout_json
            return b

        content_blocks = self.current_output["content_blocks"]

        if not block_id:

            if len(content_blocks) == 0:
                raise Exception("Cannot update most recent block: no blocks have been added yet!")

            updated_block = get_updated_block(content_blocks[-1])
            content_blocks[-1] = updated_block
            self._update_answer()
            return updated_block

        for idx, block in enumerate(self.current_output["content_blocks"]):
            if block['id'] == block_id:
                updated_block = get_updated_block(block)
                content_blocks[idx] = updated_block
                self._update_answer()
                return updated_block

        raise Exception(f"Unable to perform block update: block with id {block_id} not found!")

    def end_block(self, block_id: str = None) -> ContentBlock:
        """
        Marks the specified content block as complete, removing its loading info.
        If no block_id is provided, the last block to be added will be marked as complete.

        :param block_id: The id of the block to mark as complete, if none is provided the last block to be added will be marked as complete
        """

        if not block_id:
            block_id = self.current_output["content_blocks"][-1]['id']

        for block in self.current_output["content_blocks"]:
            if block['id'] == block_id:
                block['loading_info'] = None
                self._update_answer()
                return block

        raise Exception(f"Unable to perform block update: block with id {block_id} not found!")

    def merge_output(self, changes: ChatReportOutput) -> ChatReportOutput:
        """
        Merges the provided changes into the current report output.
        """
        self.current_output.update(changes)
        self._update_answer()
        return self.current_output
