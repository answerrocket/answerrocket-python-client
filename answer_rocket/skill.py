import os

from mypy_extensions import Arg
from sgqlc.types import non_null, Variable

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import JSON, String, UUID
from answer_rocket.output import ChatReportOutput
from answer_rocket.graphql.schema import UUID as GQL_UUID


class Skill:
    """
    Provides tools to interact with copilot skills directly.
    """

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient):
        self._auth_helper = auth_helper
        self._gql_client = gql_client

    def run(self, copilot_id: str, skill_name: str, parameters: dict | None = None) -> ChatReportOutput:
        """
        Runs a skill and returns its full output (does not stream intermediate skill output).

        copilot_id: the id of the copilot to run the skill on
        skill_name: the name of the skill to execute
        parameters: a dict of parameters to pass to the skill where keys are the param keys and values are the values
         to populate them with
        """

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

        result = self._gql_client.submit(operation, preview_query_args)

        return result.run_copilot_skill
