import json
import os
import uuid
from typing import Any, List

import sgqlc
from sgqlc.types import Arg, Variable
from typing_extensions import TypedDict
from answer_rocket.auth import AuthHelper
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


# If this code is execution on a real AR instance, is will be able to access resources where the answers are stored
IS_LIVE_RUN = os.getenv("AR_IS_RUNNING_ON_FLEET")


class OutputBuilder:

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient):
        self._auth_helper = auth_helper
        self._gql_client = gql_client
        self.answer_id = os.getenv('AR_ANSWER_ID')
        self.current_output = ChatReportOutput(
            payload=None,
            content_blocks=[],
            suggestions=[],
            interpretation_notes=[],
            final_message="",
            info=None
        )

    def _update_answer(self):
        if self.answer_id and IS_LIVE_RUN:
            query_args = {
                'answerId': self.answer_id,
                'payload': self.current_output
            }
            query_vars = {
                'answer_id': Arg(sgqlc.types.non_null(GQL_UUID)),
                'payload': Arg(sgqlc.types.non_null(JSON))
            }

            operation = self._gql_client.mutation(variables=query_vars)

            update_mutation = operation.update_chat_answer_payload(
                answer_id=Variable('answer_id'),
                payload=Variable('payload'),
            )

            self._gql_client.submit(operation, query_args)

    def add_block(self, title: str = None, loading_status: ChatLoadingInfo = None, xml: str = None,
                  is_collapsible: bool = True) -> str:
        """
        Adds a new content block to the report output. The newly added blocks becomes the default block for
        future updates until a new block is added.

        :param title: The user-friendly name of the block that will be displayed on the frontend
        :param loading_status: The loading state of the block
        :param xml: XML payload for the block to display, represented as a string.
        :param is_collapsible: Whether the block can be collapsed by the user
        """
        new_block = ContentBlock(id=str(uuid.uuid4()), title=title, loading_info=loading_status, payload=xml,
                                 is_collapsible=is_collapsible)
        self.current_output["content_blocks"].append(new_block)
        self._update_answer()
        return new_block['id']

    def update_block(self, block_id: UUID = None, title: str = None, loading_info: ChatLoadingInfo = None,
                     xml: str = None, is_collapsible: bool = None) -> ContentBlock:
        """
        Updates the specified content block with any or all of the provided parameters. If no block_id is provided,
        the last block to be added will be updated.

        :param block_id: The id of the block to update, if none is provided the last block to be added will be updated
        :param title: The user-friendly name of the block that will be displayed on the frontend, leave blank for no-update
        :param loading_info: The loading state of the block, leave blank for no-update
        :param xml: XML payload for the block to display, represented as a string, leave blank for no-update
        :param is_collapsible: Whether the block can be collapsed by the user, leave blank for no-update
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
