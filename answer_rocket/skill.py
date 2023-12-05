from sgqlc.types import Arg, non_null, Variable
from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import JSON, String, UUID
from answer_rocket.output import ChatReportOutput
from answer_rocket.graphql.schema import UUID as GQL_UUID
from answer_rocket.types import MaxResult, RESULT_EXCEPTION_CODE


class RunSkillResult(MaxResult):
    data: ChatReportOutput


class Skill:
    """
    Provides tools to interact with copilot skills directly.
    """

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient):
        self._auth_helper = auth_helper
        self._gql_client = gql_client

    def run(self, copilot_id: str, skill_name: str, parameters: dict | None = None) -> RunSkillResult:
        """
        Runs a skill and returns its full output (does not stream intermediate skill output).

        :param copilot_id: the id of the copilot to run the skill on
        :param skill_name: the name of the skill to execute
        :param parameters: a dict of parameters to pass to the skill where keys are the param keys and values are the values
         to populate them with
        :return the full output object of the skill
        """

        final_result = RunSkillResult()

        preview_query_args = {
            "copilotId": UUID(copilot_id),
            "skillName": skill_name,
            'parameters': parameters or {},
        }

        preview_query_vars = {
            'copilot_id': Arg(non_null(GQL_UUID)),
            'skill_name': Arg(non_null(String)),
            'parameters': Arg(JSON),
        }

        operation = self._gql_client.query(variables=preview_query_vars)

        preview_query = operation.run_copilot_skill(
            copilot_id=Variable('copilot_id'),
            skill_name=Variable('skill_name'),
            parameters=Variable('parameters'),
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
