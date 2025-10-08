from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.sdk_operations import Operations


class DynamicLayouts:
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

        Args:
            id (str): The UUID of the dynamic layout to retrieve.

        Returns:
            The dynamic layout data from the server.
        """
        try:
            op = Operations.query.get_dynamic_layout
            result = self._gql_client.submit(op, {
                'id': id,
            })

            return result.get_dynamic_layout
            
        except Exception as e:
            raise Exception(f"Failed to get dynamic layout: {e}")
