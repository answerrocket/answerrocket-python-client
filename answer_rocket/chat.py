import os
import logging
from typing import Literal, Callable, Optional

import openai
from sgqlc.types import Variable, non_null, String, Arg
from sgqlc.operation import Fragment

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import (LLMApiConfig, AzureOpenaiCompletionLLMApiConfig,
                                          AzureOpenaiEmbeddingLLMApiConfig, OpenaiCompletionLLMApiConfig,
                                          OpenaiEmbeddingLLMApiConfig)

logger = logging.getLogger(__name__)

ModelType = Literal['GPT3_5', 'GPT4', 'Embedding']
ApiType = Literal['AZURE', 'OPENAI']

LLMConfigType = LLMApiConfig | AzureOpenaiEmbeddingLLMApiConfig | AzureOpenaiCompletionLLMApiConfig | \
                OpenaiCompletionLLMApiConfig | OpenaiEmbeddingLLMApiConfig


class Chat:
    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient):
        self.auth_helper = auth_helper
        self.gql_client = gql_client

    def _get_llm_config(self, model_type: ModelType):
        llm_config_query_args = {
            'modelType': model_type,
        }
        llm_config_query_vars = {
            'model_type': Arg(non_null(String)),
        }
        operation = self.gql_client.query(variables=llm_config_query_vars)
        llm_config_query = operation.llmapi_config_for_sdk(
            model_type=Variable('model_type'),
        )

        llm_config_fragments = _create_llm_config_fragments()

        for fragment in llm_config_fragments:
            llm_config_query.__fragment__(fragment)

        llm_config_query.api_type()
        llm_config_query.model_type()
        llm_config_query.model_name()

        try:
            result = self.gql_client.submit(operation, llm_config_query_args)
            return result.llmapi_config_for_sdk
        except Exception as e:
            logger.error("failed to get LLM config", exc_info=True)

    def completion(self, model_type: ModelType = 'GPT3_5', stream_callback: Optional[Callable] = None, **kwargs):
        """
        Wrapper for the OpenAI chat completion API. This will attempt to retry requests.
        See here for documentation on the wrapped call: https://platform.openai.com/docs/api-reference/chat/create
        :param model_type: LLM model type to use. One of GPT3_5, GPT4, Embedding
        :param stream_callback: if provided, a function that will be called with the stream response each time one is
            received

        :param kwargs: any other arguments to pass to the underlying Completion call. Note that this method will attempt
            to fetch the appropriate config from the remote AnswerRocket instance, but you can override them by
            providing explicit arguments. It will __not__ fetch the API key. When running locally, you must provide this
            yourself in the OPENAI_API_KEY env var that the openai sdk expects you to set.
            Note that kwarg "messages" can be a string for simple completion or a list of role/content message objects for a full conversation history

        :return: success indicator (true/false), and a result which is an error string if success is false, or the assistant's reply object if success is true
        """
        llm_api_config = self._get_llm_config(model_type=model_type)
        mapped_api_args = _map_llm_api_config_parameters(llm_api_config=llm_api_config, model_type=model_type)

        args = {
            **mapped_api_args,
            **kwargs
        }

        if stream_callback:
            args["stream"] = True
        else:
            args["stream"] = False

        if isinstance(args.get("messages"), str):
            args["messages"] = [{"role": "system", "content":args["messages"] }]

        import time
        dead_man = 3
        error_backoff_multiplier = 1.5
        retry_sleep_time = 1

        last_error = None

        while dead_man > 0:
            dead_man -= 1
            try:
                gpt_res = openai.ChatCompletion.create(**args)

                if not args.get("stream"):
                    return True, gpt_res

                # rebuild the response data structure from streaming delta chunks
                response = {}
                for chunk in gpt_res:
                    if not chunk.get('choices'):
                        continue
                    delta = chunk['choices'][0]['delta']
                    for key in delta:
                        if key not in response:
                            response[key] = delta[key]
                        else:
                            if isinstance(delta[key], str):
                                response[key] += delta[key]
                            elif isinstance(delta[key], dict):
                                for inner_key in delta[key]:
                                    if inner_key not in response[key]:
                                        response[key][inner_key] = delta[key][inner_key]
                                    else:
                                        if isinstance(response[key][inner_key], str):
                                            response[key][inner_key] += delta[key][inner_key]

                        # stream to the callback if found
                        if key == "content" and delta[key] is not None and stream_callback:
                            stream_callback(delta[key])

                if not response.get("content"):
                    response["content"] = ""

                return True, {"choices": [{"message": response}]}

            # there was commented out code here that was checking for specific openai errors, but I assume it was
            # difficult to know which errors warranted abandoning early vs which just meant we should try again
            except Exception as e:
                time.sleep(retry_sleep_time)
                last_error = e
                retry_sleep_time *= error_backoff_multiplier

        return False, str(last_error)


def _create_llm_config_fragments():
    azure_completion_fragment = Fragment(AzureOpenaiCompletionLLMApiConfig, 'AzureCompletionFragment')
    azure_completion_fragment.__fields__(__exclude__=['id', 'api_type', 'model_type', 'model_name'])

    azure_embedding_fragment = Fragment(AzureOpenaiEmbeddingLLMApiConfig, 'AzureEmbeddingFragment')
    azure_embedding_fragment.__fields__(__exclude__=['id', 'api_type', 'model_type', 'model_name'])

    openai_completion_fragment = Fragment(OpenaiCompletionLLMApiConfig, 'OpenAiCompletionFragment')
    openai_completion_fragment.__fields__(__exclude__=['id', 'api_type', 'model_type', 'model_name'])

    openai_embedding_fragment = Fragment(OpenaiEmbeddingLLMApiConfig, 'OpenAiEmbeddingFragment')
    openai_embedding_fragment.__fields__(__exclude__=['id', 'api_type', 'model_type', 'model_name'])

    return [
        azure_completion_fragment,
        azure_embedding_fragment,
        openai_embedding_fragment,
        openai_completion_fragment
    ]


def _map_llm_api_config_parameters(llm_api_config: LLMConfigType, model_type: ModelType = 'GPT3_5'):
    """
    Maps the LLM Api config to the parameters for openai calls.
    """
    kwargs = {
        "api_key": os.getenv('OPENAI_API_KEY')
    }

    if llm_api_config.api_type == 'AZURE':
        kwargs.update({
            "engine": llm_api_config.model_name,
            "api_base": llm_api_config.api_base_url,
            "api_version": llm_api_config.api_version,
            "api_type": llm_api_config.api_type,
        })
    elif llm_api_config.api_type == 'OPENAI':
        kwargs.update({
            "model": llm_api_config.model_name,
            "organization": llm_api_config.organization
        })
    else:
        raise Exception("Invalid LLM config: Unknown api_type")

    if model_type == 'GPT3_5' or model_type == 'GPT4':
        kwargs.update({
            "max_tokens": llm_api_config.max_tokens_content_generation,
            "temperature": llm_api_config.temperature,
            "top_p": llm_api_config.top_p,
            "frequency_penalty": llm_api_config.frequency_penalty,
            "presence_penalty": llm_api_config.presence_penalty,
            "stop": llm_api_config.stop_sequence,
        })

    return kwargs
