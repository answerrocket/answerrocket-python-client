from dataclasses import dataclass

from sgqlc.types import Arg, non_null, Variable
from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import JSON, String, UUID, Boolean
from answer_rocket.graphql.sdk_operations import Operations
from answer_rocket.output import ChatReportOutput
from answer_rocket.graphql.schema import UUID as GQL_UUID
from answer_rocket.types import MaxResult, RESULT_EXCEPTION_CODE


@dataclass
class RunSkillResult(MaxResult):
    data: ChatReportOutput | None = None


class Skill:
    """
    Provides tools to interact with copilot skills directly.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient):
        self._config = config
        self._gql_client = gql_client

    def run(self, copilot_id: str, skill_name: str, parameters: dict | None = None, validate_parameters: bool = False, tool_definition: dict | None = None) -> RunSkillResult:
        """
        Runs a skill and returns its full output (does not stream intermediate skill output).

        :param copilot_id: the id of the copilot to run the skill on
        :param skill_name: the name of the skill to execute
        :param parameters: a dict of parameters to pass to the skill where keys are the param keys and values are the values
         to populate them with
        :param validate_parameters: boolean switch which applies guardrails to the parameters before the skill is run
        :param tool_definition: a dictionary of the hydrated report corresponding to the skill.b Can be fetched from config.get_copilot_hydrated_reports. Required when validate_parameters is True


        :return the full output object of the skill
        """

        if validate_parameters and tool_definition is None:
            raise ValueError("tool_definition is required when validate_parameters is True")

        final_result = RunSkillResult(None)

        preview_query_args = {
            "copilotId": UUID(copilot_id),
            "skillName": skill_name,
            'parameters': parameters or {},
            'validateParameters': validate_parameters,
            'toolDefinition': tool_definition or {},
        }

        preview_query_vars = {
            'copilot_id': Arg(non_null(GQL_UUID)),
            'skill_name': Arg(non_null(String)),
            'parameters': Arg(JSON),
            'validate_parameters': Arg(Boolean),
            'tool_definition': Arg(JSON),
        }

        operation = self._gql_client.query(variables=preview_query_vars)

        preview_query = operation.run_copilot_skill(
            copilot_id=Variable('copilot_id'),
            skill_name=Variable('skill_name'),
            parameters=Variable('parameters'),
            validate_parameters=Variable('validate_parameters'),
            tool_definition=Variable('tool_definition'),
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

    def update_loading_message(self, message: str):
        if self._config.entry_answer_id:
            args = {
                'answerId': self._config.entry_answer_id,
                'message': message,
                'nudgeEntryId': self._config.chat_entry_id,
            }
            op = Operations.mutation.update_loading_message
            self._gql_client.submit(op, args)
