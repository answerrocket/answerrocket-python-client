import logging
from datetime import datetime
from typing import Literal
from sgqlc.types import Variable, non_null, String, Arg, list_of

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import (LLMApiConfig, AzureOpenaiCompletionLLMApiConfig,
                                          AzureOpenaiEmbeddingLLMApiConfig, OpenaiCompletionLLMApiConfig,
                                          OpenaiEmbeddingLLMApiConfig, UUID, Int, DateTime, ChatDryRunType,
                                          MaxChatEntry, MaxChatThread, SharedThread, MaxChatUser)
from answer_rocket.graphql.sdk_operations import Operations

logger = logging.getLogger(__name__)

FeedbackType = Literal['CHAT_POSITIVE', 'CHAT_NEGATIVE']


class Chat:
    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient):
        self.auth_helper = auth_helper
        self.gql_client = gql_client

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
    
    def add_feedback(self, entry_id: str, feedback_type: FeedbackType, feedback_text: str = None) -> bool:
        """
        This adds feedback to a chat entry.
        :param entry_id: the id of the chat entry
        :param feedback_type: the type of feedback to add
        :param feedback_text: the text of the feedback
        :return: True if the feedback was added successfully, False otherwise
        """

        add_feedback_mutation_args = {
            'entryId': UUID(entry_id),
            'feedbackType': feedback_type,
            'message': feedback_text
        }
        op = Operations.mutation.add_feedback
        result = self.gql_client.submit(op, add_feedback_mutation_args)

        return result.add_feedback

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

    def get_user(self, user_id: str) -> MaxChatUser:
        """
        This fetches a user by their ID.
        :param user_id: the id of the user
        :return: A MaxChatUser object
        """

        get_user_query_args = {
            'id': UUID(user_id)
        }
        get_user_query_vars = {
            'id': Arg(non_null(UUID))
        }
        operation = self.gql_client.query(variables=get_user_query_vars)
        get_users_query = operation.user(
            id=Variable('id')
        )

        result = self.gql_client.submit(operation, get_user_query_args)

        return result.user

    def get_all_chat_entries(self, offset=0, limit=100, filters=None) -> list[MaxChatEntry]:
        """
        Fetches all chat entries with optional filters.
        :param offset: the offset to start fetching entries from. Default is 0.
        :param limit: the maximum number of entries to fetch. Default is 100.
        :param filters: a dictionary of filters to apply to the query. Supports all filtering available in the query browser.

        Example Filter after a date:

        {
            "askedDate": {
              "dateFrom": "2024-10-25 00:00:00",
              "dateTo": None,
              "filterType": "date",
              "type": "askedAfter"
            }
        }

        Other available fields:

        {
            "askedDate": {
              "dateFrom": "2024-10-25 00:00:00",
              "dateTo": "2025-10-26 00:00:00",
              "filterType": "date",
              "type": "askedBetween"
            },
            "questionType": {
              "values": [
                "Test Runs",
                "User Written"
              ],
              "filterType": "set"
            },
            "username": {
              "values": ["someusername"],
              "filterType": "set"
            },
            "lastName": {
              "values": ["somelastname"],
              "filterType": "set"
            },
            "firstName": {
              "values": ["somefirstname"],
              "filterType": "set"
            },
            "copilot": {
              "values": [
                "My Copilot"
              ],
              "filterType": "set"
            },
            "copilotSkillName": {
              "values": [
                "Dimension Breakout",
                "globals test",
                "Document Explorer",
                "Trend Analysis"
              ],
              "filterType": "set"
            },
            "type": {
              "values": [
                "Positive"
              ],
              "filterType": "set"
            },
            "feedbackReviewed": {
              "values": [
                "Seen"
              ],
              "filterType": "set"
            },
            "adminFeedback": {
              "values": [
                "Negative"
              ],
              "filterType": "set"
            },
            "status": {
              "values": [
                "error",
                "completed",
                "canceled",
                "processing"
              ],
              "filterType": "set"
            }
          }


        :return: a list of ChatEntry objects
        """
        get_all_chat_entries_query_args = {
            'offset': offset,
            'limit': limit,
            'filters': filters,
        }

        operation = Operations.query.all_chat_entries

        result = self.gql_client.submit(operation, get_all_chat_entries_query_args)

        return result.all_chat_entries
