import abc
from dataclasses import dataclass

from answer_rocket.client_config import ClientConfig
from answer_rocket.error import AnswerRocketClientError


@dataclass
class AuthHelper(abc.ABC):
	"""
	Helper for producing the appropriate headers to auth with an AnswerRocket server.
	Creating one is handled by the client automatically.
	"""
	config: ClientConfig

	@abc.abstractmethod
	def headers(self) -> dict:
		pass


@dataclass
class ExternalAuthHelper(AuthHelper):

	def headers(self) -> dict:
		headers = {
			'Authorization': f'Bearer {self.config.token}'
		}
		if self.config.user_id:
			headers['Max-User'] = self.config.user_id
		if self.config.tenant:
			headers['Max-Tenant'] = self.config.tenant
		return headers
	

@dataclass
class InternalAuthHelper(AuthHelper):

	def headers(self) -> dict:
		headers = {
			'Max-Tenant': self.config.tenant,
			'Authorization': 'Max-Internal',
		}
		if self.config.user_id:
			headers['Max-User'] = self.config.user_id
		return headers
	

def init_auth_helper(config: ClientConfig) -> AuthHelper:
	if not config.url:
		raise AnswerRocketClientError('No AnswerRocket url provided')
	if config.token:
		return ExternalAuthHelper(config)
	return InternalAuthHelper(config)
