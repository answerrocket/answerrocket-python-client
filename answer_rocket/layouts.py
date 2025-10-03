from typing import Optional
from sgqlc.types import Variable, Arg, non_null, String
from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID


class Layouts:
    """
    Helper for accessing config, whether local or fetched from the configured server.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        self._gql_client = gql_client
        self._config = config
        self.copilot_id = self._config.copilot_id
        self.copilot_skill_id = self._config.copilot_skill_id

    def get_dynamic_layout(self, id: str):
        """
        Get a dynamic layout by id.
    
        id : str
            The UUID of the dynamic layout to retrieve.
    
        """
        op = Operations.query.get_dynamic_layout
        self._gql_client.submit(op, {
            'id': id,
        })

        return result.get_dynamic_layout
