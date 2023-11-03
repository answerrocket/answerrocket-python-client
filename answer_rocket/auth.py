import abc
import os
from dataclasses import dataclass
from typing import Optional

from answer_rocket.error import AnswerRocketClientError


class AuthHelper(abc.ABC):
	"""
	Helper for producing the appropriate headers to auth with an AnswerRocket server.
	Creating one is handled by the client automatically.
	"""
	url: str

	@abc.abstractmethod
	def headers(self) -> dict:
		pass


@dataclass
class ExternalAuthHelper(AuthHelper):
	url: str
	token: str

	def headers(self) -> dict:
		return {
			'Authorization': f'Bearer {self.token}'
		}
	

@dataclass
class InternalAuthHelper(AuthHelper):
	url: str
	tenant: str
	user: str | None

	def headers(self) -> dict:
		headers = {
			'Max-Tenant': self.tenant,
			'Authorization': 'Max-Internal',
		}
		if self.user:
			headers['Max-User'] = self.user
		return headers
	

def init_auth_helper(url: Optional[str], token: Optional[str]) -> AuthHelper:
	token = token or os.getenv('AR_TOKEN')
	url = url or os.getenv('AR_URL')
	if not url:
		raise AnswerRocketClientError('No AnswerRocket url provided')
	if token:
		return ExternalAuthHelper(url=url, token=token)
	tenant = os.getenv('AR_TENANT_ID')
	user = os.getenv('AR_USER_ID')
	return InternalAuthHelper(url=url, tenant=tenant, user=user)