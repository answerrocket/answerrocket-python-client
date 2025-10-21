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
	"""
	Authentication helper for external API access using bearer tokens.
	"""

	def headers(self) -> dict:
		"""
		Generate authentication headers for external API requests.

		Returns
		-------
		dict
			Dictionary containing Authorization header and optional Max-User/Max-Tenant headers.
		"""
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
	"""
	Authentication helper for internal service-to-service communication.
	"""

	def headers(self) -> dict:
		"""
		Generate authentication headers for internal service requests.

		Returns
		-------
		dict
			Dictionary containing Max-Internal authorization and optional Max-User/Max-Tenant headers.
		"""
		headers = {
			'Max-Tenant': self.config.tenant,
			'Authorization': 'Max-Internal',
		}
		if self.config.user_id:
			headers['Max-User'] = self.config.user_id
		return headers
	

def init_auth_helper(config: ClientConfig) -> AuthHelper:
	"""
	Initialize the appropriate authentication helper based on configuration.

	Parameters
	----------
	config : ClientConfig
		The client configuration containing authentication details.

	Returns
	-------
	AuthHelper
		ExternalAuthHelper if token is provided, otherwise InternalAuthHelper.

	Raises
	------
	AnswerRocketClientError
		If no AnswerRocket URL is provided in the configuration.
	"""
	if not config.url:
		raise AnswerRocketClientError('No AnswerRocket url provided')
	if config.token:
		return ExternalAuthHelper(config)
	return InternalAuthHelper(config)
