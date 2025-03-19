import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    """
    Class that holds all client config.
    Attributes:
        url: environment url
        token: an auth token
        tenant: the tenant id, provided automatically
        is_live_run: set when the client is used in a skill run (as opposed to someone running it locally)
        answer_id: the skill run answer_id that any answer-updating calls will use
        entry_answer_id: the answer_id for the chat entry being created
        user_id: provided automatically or implicitly via the auth token
        copilot_id: the copilot the skill is running within
        copilot_skill_id: the id of the skill in the environment
        resource_base_path: the base path to use for resources
    """
    url: str
    token: str | None
    tenant: str | None
    is_live_run: bool
    answer_id: str | None
    entry_answer_id: str | None
    user_id: str | None
    copilot_id: str | None
    copilot_skill_id: str | None
    resource_base_path: str | None
    thread_id: str | None
    chat_entry_id: str | None


def load_client_config(url=None, token=None, tenant: str = None):
    token = token or os.getenv('AR_TOKEN')
    url = url or os.getenv('AR_URL')
    effective_tenant = tenant if tenant else os.getenv('AR_TENANT_ID')
    user_id = os.getenv('AR_USER_ID')
    answer_id = os.getenv('AR_ANSWER_ID')
    entry_answer_id = os.getenv('AR_ENTRY_ANSWER_ID')
    copilot_id = os.getenv('AR_COPILOT_ID')
    copilot_skill_id = os.getenv('AR_COPILOT_SKILL_ID')
    is_live_run = os.getenv('AR_IS_RUNNING_ON_FLEET') or False
    resource_base_path = os.getenv('AR_SKILL_RESOURCE_BASE_PATH')
    thread_id = os.getenv('AR_THREAD_ID')
    chat_entry_id = os.getenv('AR_CHAT_ENTRY_ID')
    return ClientConfig(
        url=url,
        token=token,
        tenant=effective_tenant,
        user_id=user_id,
        is_live_run=is_live_run,
        answer_id=answer_id,
        entry_answer_id=entry_answer_id,
        copilot_id=copilot_id,
        copilot_skill_id=copilot_skill_id,
        resource_base_path=resource_base_path,
        thread_id=thread_id,
        chat_entry_id=chat_entry_id
    )

