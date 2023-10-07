from typing import Optional

from answer_rocket.auth import AuthHelper, init_auth_helper
from answer_rocket.config import Config
from answer_rocket.graphql.client import GraphQlClient


class AnswerRocketClient:

	def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
		"""
		url: the url of your AnswerRocket instance. You may also set the AR_URL env var instead.
		token: a valid sdk token. You may also set the AR_TOKEN env var instead to keep it out of your code.
		"""
		self._auth_helper: AuthHelper = init_auth_helper(url=url, token=token)
		self._gql_client: GraphQlClient = GraphQlClient(self._auth_helper)
		self.config = Config(self._auth_helper, self._gql_client)

	def can_connect(self) -> bool:
		"""
		utility method for checking that the client can connect to and authenticate with the server it is pointed at
		"""
		ping_op = self._gql_client.query()
		ping_op.ping()
		result = self._gql_client.submit(ping_op)
		return result.ping == 'pong'
