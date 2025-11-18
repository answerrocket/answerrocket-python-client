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
        group_ids: Optional[List[UUID]] = None,
        body_format: Optional[str] = None
    ) -> EmailSendResponse:
        """
        Send an email to specified users and/or groups.

        Parameters
        ----------
        subject : str
            The email subject line.
        body : str
            The email body content. Format depends on body_format parameter.
        user_ids : List[UUID], optional
            List of user IDs to send the email to.
        group_ids : List[UUID], optional
            List of group IDs to send the email to. All members of these groups will receive the email.
        body_format : str, optional
            The format of the email body. Valid values are 'HTML' or 'PLAIN_TEXT'.
            Defaults to 'HTML' if not specified.

        Returns
        -------
        EmailSendResponse
            Response object containing:
            - success: bool - Whether the email was sent successfully
            - recipient_count: int - Number of recipients the email was sent to
            - error: str - Error message if the operation failed

        Examples
        --------
        Send an HTML email to specific users:

        >>> result = max.email.send_email(
        ...     user_ids=[uuid.UUID("12345678-1234-1234-1234-123456789abc")],
        ...     subject="Test Email",
        ...     body="<h1>Hello!</h1><p>This is a test.</p>",
        ...     body_format="HTML"
        ... )
        >>> print(f"Sent to {result.recipient_count} recipients")

        Send a plain text email to a group:

        >>> result = max.email.send_email(
        ...     group_ids=[uuid.UUID("11111111-1111-1111-1111-111111111111")],
        ...     subject="Group Notification",
        ...     body="This is a plain text notification.",
        ...     body_format="PLAIN_TEXT"
        ... )
        """
        mutation_args = {
            'userIds': [str(uid) for uid in user_ids] if user_ids else None,
            'groupIds': [str(gid) for gid in group_ids] if group_ids else None,
            'subject': subject,
            'body': body,
            'bodyFormat': body_format,
        }

        op = Operations.mutation.send_email
        result = self._gql_client.submit(op, mutation_args)

        return result.send_email
