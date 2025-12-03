from dataclasses import dataclass

from sgqlc.types import Arg, non_null, Variable
from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import JSON, String, UUID, Boolean, AsyncSkillStatusResponse
from answer_rocket.graphql.sdk_operations import Operations
from answer_rocket.output import ChatReportOutput
from answer_rocket.graphql.schema import UUID as GQL_UUID
from answer_rocket.types import MaxResult, RESULT_EXCEPTION_CODE


@dataclass
class RunSkillResult(MaxResult):
    """
    Result object for synchronous skill execution.

    Attributes
    ----------
    data : ChatReportOutput | None
        The output data from the skill execution.
    """
    data: ChatReportOutput | None = None

    def __init__(self, success: bool = False, **kwargs):
        super().__init__(success, **kwargs)
        self.data = kwargs.get('data')


@dataclass
class AsyncSkillRunResult(MaxResult):
    """
    Result object for asynchronous skill execution.

    Attributes
    ----------
    execution_id : str | None
        The unique execution ID for tracking the async skill run.
    """
    execution_id: str | None = None

    def __init__(self, success: bool = False, **kwargs):
        super().__init__(success, **kwargs)
        self.execution_id = kwargs.get('execution_id')


class Skill:
    """
    Provides tools to interact with copilot skills directly.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient):
        """
        Initialize the Skill client.

        Parameters
        ----------
        config : ClientConfig
            The client configuration.
        gql_client : GraphQlClient
            The GraphQL client for API communication.
        """
        self._config = config
        self._gql_client = gql_client

    def run(self, copilot_id: str, skill_name: str, parameters: dict | None = None, validate_parameters: bool = False) -> RunSkillResult:
        """
        Run a skill synchronously and return its full output.

        Does not stream intermediate skill output.

        Parameters
        ----------
        copilot_id : str
            The ID of the copilot to run the skill on.
        skill_name : str
            The name of the skill to execute.
        parameters : dict | None, optional
            Dictionary of parameters to pass to the skill.
        validate_parameters : bool, optional
            Whether to apply guardrails to parameters before execution. Defaults to False.

        Returns
        -------
        RunSkillResult
            The full output object of the skill execution.
        """

        final_result = RunSkillResult(None)

        preview_query_args = {
            "copilotId": UUID(copilot_id),
            "skillName": skill_name,
            'parameters': parameters or {},
            'validateParameters': validate_parameters,
        }

        preview_query_vars = {
            'copilot_id': Arg(non_null(GQL_UUID)),
            'skill_name': Arg(non_null(String)),
            'parameters': Arg(JSON),
            'validate_parameters': Arg(Boolean),
        }

        operation = self._gql_client.query(variables=preview_query_vars)

        preview_query = operation.run_copilot_skill(
            copilot_id=Variable('copilot_id'),
            skill_name=Variable('skill_name'),
            parameters=Variable('parameters'),
            validate_parameters=Variable('validate_parameters'),
        )

        try:

            result = self._gql_client.submit(operation, preview_query_args)

            preview_query.success()
            preview_query.code()
            preview_query.errors()
            preview_query.data()

            skill_run_result = result.run_copilot_skill

            final_result.success = skill_run_result.success
            final_result.error = skill_run_result.errors
            final_result.code = skill_run_result.code

            if skill_run_result.data:
                final_result.data = skill_run_result.data

        except Exception as e:
            final_result.success = False
            final_result.error = str(e)
            final_result.code = RESULT_EXCEPTION_CODE

        return final_result

    def run_async(self, copilot_id: str, skill_name: str, parameters: dict | None = None) -> AsyncSkillRunResult:
        """
        Start a skill execution asynchronously and return an execution ID immediately.

        Parameters
        ----------
        copilot_id : str
            The ID of the copilot to run the skill on.
        skill_name : str
            The name of the skill to execute.
        parameters : dict | None, optional
            Dictionary of parameters to pass to the skill.

        Returns
        -------
        AsyncSkillRunResult
            Result containing execution_id if successful.
        """
        try:
            async_query_args = {
                "copilotId": UUID(copilot_id),
                "skillName": skill_name,
                'parameters': parameters or {}
            }

            op = Operations.mutation.run_copilot_skill_async

            result = self._gql_client.submit(op, async_query_args)

            skill_run_result = result.run_copilot_skill_async

            final_result = AsyncSkillRunResult()
            final_result.success = skill_run_result.success
            final_result.error = skill_run_result.error
            final_result.code = skill_run_result.code
            final_result.execution_id = skill_run_result.execution_id

            return final_result
        except Exception as e:
            final_result = AsyncSkillRunResult()
            final_result.success = False
            final_result.error = str(e)
            final_result.code = RESULT_EXCEPTION_CODE
            return final_result

    def get_async_status(self, execution_id: str) -> AsyncSkillStatusResponse:
        """
        Get the status and result of an async skill execution.

        Parameters
        ----------
        execution_id : str
            The execution ID returned from run_async.

        Returns
        -------
        AsyncSkillStatusResponse
            Result with status and data if completed, None if error occurs.
        """
        try:

            status_query_args = {
                "executionId": execution_id,
            }

            op = Operations.query.get_async_skill_run_status

            result = self._gql_client.submit(op, status_query_args)

            return result.get_async_skill_run_status
        except Exception as e:
            print(e)
            return None

    def update_loading_message(self, message: str):
        """
        Update the loading message for the current skill execution.

        Parameters
        ----------
        message : str
            The loading message to display to the user.
        """
        if self._config.entry_answer_id:
            args = {
                'answerId': self._config.entry_answer_id,
                'message': message,
                'nudgeEntryId': self._config.chat_entry_id,
            }
            op = Operations.mutation.update_loading_message
            self._gql_client.submit(op, args)
