from typing import Optional

from answer_rocket.client_config import load_client_config
from answer_rocket.config import Config
from answer_rocket.data import Data
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.chat import Chat
from answer_rocket.output import OutputBuilder
from answer_rocket.skill import Skill
from answer_rocket.llm import Llm


class AnswerRocketClient:

	def __init__(self, url: Optional[str] = None, token: Optional[str] = None, tenant: str = None):
		"""
		url: the url of your AnswerRocket instance. You may also set the AR_URL env var instead.
		token: a valid sdk token. You may also set the AR_TOKEN env var instead to keep it out of your code.
		"""
		self._client_config = load_client_config(url, token, tenant)
		self._gql_client: GraphQlClient = GraphQlClient(self._client_config)
		self.config = Config(self._client_config, self._gql_client)
		self.chat = Chat(self._gql_client, self._client_config)
		self.data = Data(self._client_config, self._gql_client)
		self.output = OutputBuilder(self._client_config, self._gql_client)
		self.skill = Skill(self._client_config, self._gql_client)
		self.llm = Llm(self._client_config, self._gql_client)

	def can_connect(self) -> bool:
		"""
		utility method for checking that the client can connect to and authenticate with the server it is pointed at
		"""
		ping_op = self._gql_client.query()
		ping_op.ping()
		result = self._gql_client.submit(ping_op)
		return result.ping == 'pong'
