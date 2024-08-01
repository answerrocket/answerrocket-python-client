import os
import logging
from datetime import datetime
from typing import Literal, Callable, Optional

import openai
from sgqlc.types import Variable, non_null, String, Arg, Boolean, list_of
from sgqlc.operation import Fragment

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import (LLMApiConfig, AzureOpenaiCompletionLLMApiConfig,
                                          AzureOpenaiEmbeddingLLMApiConfig, OpenaiCompletionLLMApiConfig,
                                          OpenaiEmbeddingLLMApiConfig, UUID, Int, DateTime, ChatDryRunType,
                                          MaxChatEntry, MaxChatThread, SharedThread, ModelOverride)
from answer_rocket.graphql.sdk_operations import Operations


logger = logging.getLogger(__name__)

ModelType = Literal['COMPLETION', 'EMBEDDING']
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

    def completion(self, model_type: ModelType = 'COMPLETION', stream_callback: Optional[Callable] = None, **kwargs):
        """
        Wrapper for the OpenAI chat completion API. This will attempt to retry requests.
        See here for documentation on the wrapped call: https://platform.openai.com/docs/api-reference/chat/create
        :param model_type: LLM model type to use. One of COMPLETION, EMBEDDING
        :param stream_callback: if provided, a function that will be called with the stream response each time one is
            received

        :param kwargs: any other arguments to pass to the underlying Completion call. Note that this method will attempt
            to fetch the appropriate config from the remote AnswerRocket instance, but you can override them by
            providing explicit arguments. It will __not__ fetch the API key. When running locally, you must provide this
            yourself in the OPENAI_API_KEY env var that the openai sdk expects you to set.
            Note that kwarg "messages" can be a string for simple completion or a list of role/content message objects for a full conversation history

        :return: success indicator (true/false), and a result which is an error string if success is false, or the assistant's reply object if success is true
        """

        # Fall back to completion for old cases where model_type could be a different value such as GPT_4, etc.
        # This is for backwards compatibility... hopefully this block does not need to be used much in the future
        if model_type == 'Embedding':
            model_type: ModelType = 'EMBEDDING'
        elif model_type not in ['COMPLETION', 'EMBEDDING']:
            model_type: ModelType = 'COMPLETION'

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

    def ask_question(self, copilot_id: str, question: str, thread_id: str = None, skip_report_cache: bool = False, dry_run_type: str = None, model_overrides: dict = None, indicated_skills: list[str] = None, history: list[dict] = None):
        """
        Calls the Max chat pipeline to answer a natural language question and receive analysis and insights
        in response.
        :param copilot_id: the ID of the copilot to run the question against
        :param question: The natural language question to ask the engine.
        :param thread_id: (optional) ID of the thread/conversation to run the question on. The question and answer will
         be added to the bottom of the thread.
        :param skip_report_cache: Should the report cache be skipped for this question?
        :param dry_run_type: If provided, run a dry run at the specified level: 'SKIP_SKILL_EXEC', 'SKIP_SKILL_NLG'
        :param model_overrides: If provided, a dictionary of model types to model names to override the LLM model used. Model type options are 'CHAT', 'EMBEDDINGS', 'NARRATIVE'
        :param indicated_skills: If provided, a list of skill names that the copilot will be limited to choosing from. If only 1 skill is provided the copilot will be guaranteed to execute that skill.
        :param history: If provided, a list of messages to be used as the conversation history for the question
        :return: the ChatEntry response object associate with the answer from the pipeline
        """
        override_list = []
        if model_overrides:
            for key in model_overrides:
                override_list.append({"modelType": key, "modelName": model_overrides[key]})

        ask_question_query_args = {
            'copilotId': UUID(copilot_id),
            'question': question,
            'threadId': UUID(thread_id) if thread_id else None,
            'skipReportCache': skip_report_cache,
            'dryRunType': ChatDryRunType(dry_run_type) if dry_run_type else None,
            'modelOverrides': override_list if override_list else None,
            'indicatedSkills': indicated_skills,
            'history': history if history else None
        }

        op = Operations.mutation.ask_chat_question
        result = self.gql_client.submit(op, ask_question_query_args)

        return result.ask_chat_question

    def get_threads(self, copilot_id: str, start_date: datetime = None, end_date: datetime = None):
        """
        Fetches all threads for a given copilot and date range.
        :param copilot_id: the ID of the copilot to fetch threads for
        :param start_date: the start date of the range to fetch threads for
        :param end_date: the end date of the range to fetch threads for
        :return: a list of ChatThread IDs
        """

        def format_date(input_date: datetime):
            if not input_date:
                return None
            return str(input_date.isoformat()).replace(" ", "T") + "Z"

        get_threads_query_args = {
            'copilotId': UUID(copilot_id),
            'startDate': format_date(start_date),
            'endDate': format_date(end_date),
        }
        get_threads_query_vars = {
            'copilot_id': Arg(non_null(UUID)),
            'start_date': Arg(DateTime),
            'end_date': Arg(DateTime),
        }
        operation = self.gql_client.query(variables=get_threads_query_vars)
        get_threads_query = operation.user_chat_threads(
            copilot_id=Variable('copilot_id'),
            start_date=Variable('start_date'),
            end_date=Variable('end_date'),
        )

        result = self.gql_client.submit(operation, get_threads_query_args)

        return result.user_chat_threads

    def get_entries(self, thread_id: str, offset: int = None, limit: int = None):
        """
        Fetches all entries for a given thread.
        :param thread_id: the ID of the thread to fetch entries for
        :param offset: (optional) the offset to start fetching entries from
        :param limit: (optional) the maximum number of entries to fetch
        :return: a list of ChatEntry objects
        """
        get_entries_query_args = {
            'threadId': UUID(thread_id),
            'offset': offset,
            'limit': limit,
        }
        get_entries_query_vars = {
            'thread_id': Arg(non_null(UUID)),
            'offset': Arg(Int),
            'limit': Arg(Int),
        }
        operation = self.gql_client.query(variables=get_entries_query_vars)
        get_entries_query = operation.user_chat_entries(
            thread_id=Variable('thread_id'),
            offset=Variable('offset'),
            limit=Variable('limit'),
        )

        result = self.gql_client.submit(operation, get_entries_query_args)

        return result.user_chat_entries
    
    def evaluate_entry(self, entry_id: str, evals: list[str]):
        """
        Runs and fetches the inputted evaluations for a given entry.
        :param entry_id: the ID of the entry to fetch evaluation for
        :param evals: a list of strings containing the evaluations to run on the entry
        :return: a ChatEntryEvaluation object
        """
        evaluate_entry_mutation_args = {
            'entryId': UUID(entry_id),
            'evals': evals,
        }
        evaluate_entry_mutation_vars = {
            'entry_id': Arg(non_null(UUID)),
            'evals': Arg(non_null(list_of(non_null(String)))),
        }
        operation = self.gql_client.mutation(variables=evaluate_entry_mutation_vars)
        evaluate_entry_query = operation.evaluate_chat_question(
            entry_id=Variable('entry_id'),
            evals=Variable('evals'),
        )

        result = self.gql_client.submit(operation, evaluate_entry_mutation_args)

        return result.evaluate_chat_question

    def share_chat_thread(self, original_thread_id: str) -> SharedThread:
        mutation_args = {
            'originalThreadId': original_thread_id
        }

        mutation_vars = {
            'original_thread_id': Arg(non_null(UUID))
        }

        operation = self.gql_client.mutation(variables=mutation_vars)

        operation.share_thread(
            original_thread_id=Variable('original_thread_id')
        )
        result = self.gql_client.submit(operation, mutation_args)

        return result.share_thread

    def get_chat_entry(self, entry_id: str) -> MaxChatEntry:
        get_chat_entry_args = {
            'id': UUID(entry_id),
        }

        op = Operations.query.chat_entry
        result = self.gql_client.submit(op, get_chat_entry_args)
        return result.chat_entry

    def get_chat_thread(self, thread_id: str) -> MaxChatThread:
        get_chat_thread_args = {
            'id': UUID(thread_id),
        }

        op = Operations.query.chat_thread
        result = self.gql_client.submit(op, get_chat_thread_args)
        return result.chat_thread

    def create_new_thread(self, copilot_id: str) -> MaxChatThread:
        create_chat_thread_args = {
            'copilotId': copilot_id,
        }

        op = Operations.mutation.create_chat_thread
        result = self.gql_client.submit(op, create_chat_thread_args)
        return result.create_chat_thread

    def queue_chat_question(self, question: str, thread_id: str, skip_cache: bool = False, model_overrides: dict = None, indicated_skills: list[str] = None, history: list[dict] = None) -> MaxChatEntry:
        """
        This queues up a question for processing. Unlike ask_question, this will not wait for the processing to
        complete. It will immediately return a shell entry with an id you can use to query for the results.
        :param question: the text of the user's question
        :param thread_id: id of the thread the question is being sent to.
        :param skip_cache: Set to true to force a fresh run of the question, ignoring any existing skill result caches.
        :param model_overrides: If provided, a dictionary of model types to model names to override the LLM model used. Model type options are 'CHAT', 'EMBEDDINGS', 'NARRATIVE'
        :param indicated_skills: If provided, a list of skill names that the copilot will be limited to choosing from. If only 1 skill is provided the copilot will be guaranteed to execute that skill.
        :param history: If provided, a list of messages to be used as the conversation history for the question
        :return:
        """

        override_list = []
        if model_overrides:
            for key in model_overrides:
                override_list.append({"modelType": key, "modelName": model_overrides[key]})

        queue_chat_question_args = {
            'question': question,
            'skipCache': skip_cache,
            'threadId': thread_id,
            'modelOverrides': override_list if override_list else None,
            'indicatedSkills': indicated_skills,
            'history': history if history else None
        }

        op = Operations.mutation.queue_chat_question

        result = self.gql_client.submit(op, queue_chat_question_args)

        return result.queue_chat_question

    def cancel_chat_question(self, entry_id: str) -> MaxChatEntry:
        """
        This deletes the entry from its thread and attempts to abandon the question's processing if it is still ongoing.
        :param entry_id: the id of the chat entry
        :return: the deleted entry
        """
        cancel_chat_question_args = {
            'entryId': entry_id,
        }

        op = Operations.mutation.cancel_chat_question

        result = self.gql_client.submit(op, cancel_chat_question_args)

        return result.cancel_chat_question


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


def _map_llm_api_config_parameters(llm_api_config: LLMConfigType, model_type: ModelType = 'COMPLETION'):
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

    if model_type == 'COMPLETION':
        kwargs.update({
            "max_tokens": llm_api_config.max_tokens_content_generation,
            "temperature": llm_api_config.temperature,
            "top_p": llm_api_config.top_p,
            "frequency_penalty": llm_api_config.frequency_penalty,
            "presence_penalty": llm_api_config.presence_penalty,
            "stop": "** DONE **",
        })

    return kwargs
