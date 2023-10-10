import os
from typing import Optional

from sgqlc.types import Variable, Arg, non_null, String

from answer_rocket.auth import AuthHelper
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID

# Not clear to what degree there will be distinct "local" vs "server" modes. If there end up being 0 examples of config
# that must be grabbed from a server even while developing locally then it may make sense to have two different helpers
# rather than checking this variable in every single method.
USE_SERVER_CONFIG = os.getenv('AR_USE_SERVER_CONFIG')


class Config:
    """
    Helper for accessing config, whether local or fetched from the configured server.
    """

    def __init__(self, auth_helper: AuthHelper, gql_client: GraphQlClient) -> None:
        self._auth_helper = auth_helper
        self._gql_client = gql_client
        self.copilot_id = os.getenv('AR_COPILOT_ID')
        self.copilot_skill_id = os.getenv('AR_COPILOT_SKILL_ID')

    def get_artifact(self, artifact_path: str) -> str:
        """
        artifact path: this is the filepath to your artifact relative to the root of your project.
        Server-side overrides are keyed on this path and will be fetched first when running inside AnswerRocket
        """
        if USE_SERVER_CONFIG:
            server_artifact = self._get_artifact_from_server(artifact_path)
            if server_artifact:
                return server_artifact

        # it is possible this could be put inside an else block if the above call were changed to get either the
        # override or the base artifact if one does not exist
        with open(_complete_artifact_path(artifact_path)) as artifact_file:
            return artifact_file.read()

    def _get_artifact_from_server(self, artifact_path: str) -> Optional[dict]:
        if not self.copilot_id or not self.copilot_skill_id:
            return None
        artifact_query_args = {
            'copilotId': self.copilot_id,
            'copilotSkillId': self.copilot_skill_id,
            'artifactPath': artifact_path,
        }
        artifact_query_vars = {
            'copilot_id': Arg(non_null(GQL_UUID)),
            'copilot_skill_id': Arg(non_null(GQL_UUID)),
            'artifact_path': Arg(non_null(String)),
        }
        operation = self._gql_client.query(variables=artifact_query_vars)
        copilot_query = operation.get_copilot_skill_artifact_by_path(
            copilot_id=Variable('copilot_id'),
            copilot_skill_id=Variable('copilot_skill_id'),
            artifact_path=Variable('artifact_path'),
        )
        copilot_query.artifact()
        result = self._gql_client.submit(operation, artifact_query_args)
        if result.get_copilot_skill_artifact_by_path and result.get_copilot_skill_artifact_by_path.artifact:
            return result.get_copilot_skill_artifact_by_path.artifact


def _complete_artifact_path(artifact_path: str) -> str:
    """
    adjust the path according to the runtime env if needed.
    a noop when running locally, and possibly something we can remove entirely in the future
    """
    if os.getenv('AR_SKILL_RESOURCE_BASE_PATH'):
        return os.path.join(os.getenv('AR_SKILL_RESOURCE_BASE_PATH'), artifact_path)
    return artifact_path
