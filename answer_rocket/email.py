from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import EmailSendResponse
from answer_rocket.graphql.sdk_operations import Operations


class Email:
    """
    Helper for sending emails via the AnswerRocket platform.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        self._gql_client = gql_client
        self._config = config

    def send_email(
        self,
        subject: str,
        body: str,
        user_ids: Optional[List[UUID]] = None,
        group_ids: Optional[List[UUID]] = None
    ) -> EmailSendResponse:
        """
        Send an email to specified users and/or groups.

        Parameters
        ----------
        subject : str
            The email subject line.
        body : str
            The email body content.
        user_ids : List[UUID], optional
            List of user IDs to send the email to.
        group_ids : List[UUID], optional
            List of group IDs to send the email to. All members of these groups will receive the email.

        Returns
        -------
        EmailSendResponse
            Response object containing:
            - success: bool - Whether the email was sent successfully
            - recipient_count: int - Number of recipients the email was sent to
            - error: str - Error message if the operation failed

        Examples
        --------
        Send an email to specific users:

        >>> result = max.email.send_email(
        ...     user_ids=[uuid.UUID("12345678-1234-1234-1234-123456789abc")],
        ...     subject="Test Email",
        ...     body="Hello! This is a test email."
        ... )
        >>> print(f"Sent to {result.recipient_count} recipients")

        Send an email to a group:

        >>> result = max.email.send_email(
        ...     group_ids=[uuid.UUID("11111111-1111-1111-1111-111111111111")],
        ...     subject="Group Notification",
        ...     body="This is a notification for the group."
        ... )
        """
        mutation_args = {
            'userIds': [str(uid) for uid in user_ids] if user_ids else None,
            'groupIds': [str(gid) for gid in group_ids] if group_ids else None,
            'subject': subject,
            'body': body,
        }

        op = Operations.mutation.send_email
        result = self._gql_client.submit(op, mutation_args)

        return result.send_email
