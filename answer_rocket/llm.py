from typing import TypedDict

from answer_rocket.graphql.sdk_operations import Operations
from answer_rocket.graphql.schema import LlmModelSelection


class LlmChatMessage(TypedDict):
    """
    A chat message for passing to an LLM API
    Attributes:
        role: the role of the participant in this chat
        content: the chat message
    """
    role: str
    content: str


class Llm:

    def __init__(self, config, gql_client):
        self.config = config
        self.gql_client = gql_client

    def chat_completion(self, messages: list[LlmChatMessage], model_override: str | None = None):
        """
        Call an LLM API's chat completion endpoint with the provided messages.
        :param messages: a list of dictionaries describing each message in the chat, { "role": str, "content": str }
        :param model_override: a model name or id to use instead of a configured default
        :return: the raw response from the model api
        """
        op = Operations.query.chat_completion
        args = {
            'messages': messages,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.chat_completion

    def narrative_completion(self, prompt: str, model_override: str | None = None):
        """
        Call an LLM API's completion endpoint with the provided prompt.
        :param prompt: the prompt to send to the model
        :param model_override: a model name or id to use instead of a configured default
        :return: the raw response from the model api
        """
        op = Operations.query.narrative_completion
        args = {
            'prompt': prompt,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.narrative_completion
