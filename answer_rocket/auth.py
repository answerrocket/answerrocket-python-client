import abc
import os
from dataclasses import dataclass
from typing import Optional


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

	def headers(self) -> dict:
		headers = {
			'Max-Tenant': self.tenant,
			'Authorization': 'Max-Internal'
		}
		return headers
	

def init_auth_helper(url: Optional[str], token: Optional[str]) -> AuthHelper:
	token = token or os.getenv('AR_TOKEN')
	url = url or os.getenv('AR_URL')
	if token:
		return ExternalAuthHelper(url=url, token=token)
	tenant = os.getenv('AR_TENANT_ID')
	return InternalAuthHelper(url=url, tenant=tenant)