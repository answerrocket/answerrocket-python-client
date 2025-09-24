from typing import TypedDict

from answer_rocket.client_config import ClientConfig

from answer_rocket.graphql.sdk_operations import Operations


class LlmChatMessage(TypedDict):
    """
    A chat message for passing to an LLM API
    Attributes:
        role: the role of the participant in this chat
        content: the chat message
    """
    role: str
    content: str


class LlmFunctionProperty(TypedDict):
    """
    Property definition for LLM function parameters.

    Attributes
    ----------
    type : str
        The data type of the property.
    description : str
        Description of what the property represents.
    """
    type: str
    description: str


class LlmFunctionParameters(TypedDict):
    """
    Parameters definition for an LLM function.

    Attributes
    ----------
    type : str
        The type of parameters (typically 'object').
    properties : dict[str, LlmFunctionProperty]
        Dictionary of property definitions.
    required : list[str]
        List of required property names.
    """
    type: str
    properties: dict[str, LlmFunctionProperty]
    required: list[str]


class LlmFunction(TypedDict):
    """
    Function definition for LLM tool calling.

    Attributes
    ----------
    name : str
        The name of the function.
    description : str
        Description of what the function does.
    parameters : LlmFunctionParameters
        Parameter definitions for the function.
    """
    name: str
    description: str
    parameters: LlmFunctionParameters


class Llm:
    """
    Client for interacting with LLM APIs through AnswerRocket.
    """

    def __init__(self, config: ClientConfig, gql_client):
        """
        Initialize the LLM client.

        Parameters
        ----------
        config : ClientConfig
            The client configuration.
        gql_client : GraphQlClient
            The GraphQL client for API communication.
        """
        self.config = config
        self.gql_client = gql_client

    def chat_completion(self, messages: list[LlmChatMessage], model_override: str | None = None,
                        functions: list[LlmFunction] | None = None):
        """
        Call an LLM API's chat completion endpoint with the provided messages.

        Parameters
        ----------
        messages : list[LlmChatMessage]
            List of chat messages with role and content.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.
        functions : list[LlmFunction] | None, optional
            Available functions/tools to send to the language model.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.chat_completion
        args = {
            'messages': messages,
            'functions': functions,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.chat_completion

    def chat_completion_with_prompt(self, prompt_name: str, prompt_variables: dict,
                                    model_override: str | None = None,
                                    functions: list[LlmFunction] | None = None):
        """
        Call an LLM API's chat completion endpoint with a named prompt.

        Parameters
        ----------
        prompt_name : str
            The name of the prompt to use.
        prompt_variables : dict
            Dictionary of variables to pass to the prompt.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.
        functions : list[LlmFunction] | None, optional
            Available functions/tools to send to the language model.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.chat_completion_with_prompt
        args = {
            'promptName': prompt_name,
            'promptVariables': prompt_variables,
            'functions': functions,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }

        gql_response = self.gql_client.submit(op, args)
        return gql_response.narrative_completion

    def narrative_completion(self, prompt: str, model_override: str | None = None):
        """
        Call an LLM API's completion endpoint with the provided prompt.

        Parameters
        ----------
        prompt : str
            The prompt to send to the model.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.narrative_completion
        args = {
            'prompt': prompt,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.narrative_completion

    def narrative_completion_with_prompt(self, prompt_name: str, prompt_variables: dict,
                                         model_override: str | None = None):
        """
        Call an LLM API's completion endpoint with a named prompt.

        Parameters
        ----------
        prompt_name : str
            The name of the prompt to use.
        prompt_variables : dict
            Dictionary of variables to pass to the prompt.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.narrative_completion_with_prompt
        args = {
            'promptName': prompt_name,
            'promptVariables': prompt_variables,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.narrative_completion_with_prompt

    def sql_completion(self, messages: list[LlmChatMessage], model_override: str | None = None,
                       functions: list[LlmFunction] | None = None):
        """
        Call an LLM API's chat completion endpoint using the SQL model.

        Uses the environment's configured 'SQL' model for SQL-specific tasks.

        Parameters
        ----------
        messages : list[LlmChatMessage]
            List of chat messages with role and content.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.
        functions : list[LlmFunction] | None, optional
            Available functions/tools to send to the language model.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.sql_completion
        args = {
            'messages': messages,
            'functions': functions,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.sql_completion

    def research_completion(self, messages: list[LlmChatMessage], model_override: str | None = None,
                            functions: list[LlmFunction] | None = None):
        """
        Call an LLM API's chat completion endpoint using the Research model.

        Uses the environment's configured 'Research' model for research tasks.

        Parameters
        ----------
        messages : list[LlmChatMessage]
            List of chat messages with role and content.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.
        functions : list[LlmFunction] | None, optional
            Available functions/tools to send to the language model.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.research_completion
        args = {
            'messages': messages,
            'functions': functions,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.research_completion

    def research_completion_with_prompt(self, prompt_name: str, prompt_variables: dict,
                                        model_override: str | None = None,
                                        functions: list[LlmFunction] | None = None):
        """
        Call an LLM API's chat completion endpoint with a named prompt using the Research model.

        Uses the environment's configured 'Research' model for research tasks.

        Parameters
        ----------
        prompt_name : str
            The name of the prompt to use.
        prompt_variables : dict
            Dictionary of variables to pass to the prompt.
        model_override : str | None, optional
            Model name or ID to use instead of configured default.
        functions : list[LlmFunction] | None, optional
            Available functions/tools to send to the language model.

        Returns
        -------
        dict
            The raw response from the model API.
        """
        op = Operations.query.research_completion_with_prompt
        args = {
            'promptName': prompt_name,
            'promptVariables': prompt_variables,
            'functions': functions,
            'modelSelection': {
                'assistantId': self.config.copilot_id,
                'modelOverride': model_override
            },
            'llmMeta': {
                'answerId': self.config.answer_id,
                'threadId': self.config.thread_id,
                'copilotId': self.config.copilot_id,
                'skillId': self.config.copilot_skill_id,
            }
        }
        gql_response = self.gql_client.submit(op, args)
        return gql_response.research_completion_with_prompt
