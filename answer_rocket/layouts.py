from __future__ import annotations

from typing import Optional, Dict, Any, List
from uuid import UUID

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

    def generate_pdf_from_layouts(
        self,
        layouts: List[str]
    ):
        """
        Generate a PDF from a list of layout JSON strings.

        This is the primary method for SDK users to generate PDFs from layouts.
        Uses the same rendering infrastructure as the "Download PDF" button in the UI,
        ensuring identical output. Returns base64-encoded PDF data that can be
        directly passed to sendEmail as an attachment.

        Parameters
        ----------
        layouts : List[str]
            List of layout JSON strings to render as PDF pages.
            Each string should be a valid layout JSON representation.

        Returns
        -------
        LayoutPdfResponse
            Response object containing:
            - success: bool - Whether the PDF generation completed successfully
            - code: str - Optional status or error code
            - error: str - Human-readable error message if the operation failed
            - pdf: str - Base64-encoded PDF data, ready to use as an email attachment payload

        Examples
        --------
        Generate a PDF from a single layout:

        >>> # First, get the layout
        >>> layout = max.dynamic_layouts.get_dynamic_layout(
        ...     id="12345678-1234-1234-1234-123456789abc"
        ... )
        >>> # Generate PDF from the layout JSON
        >>> result = max.dynamic_layouts.generate_pdf_from_layouts(
        ...     layouts=[layout.layout_json]
        ... )
        >>> if result.success:
        ...     import base64
        ...     pdf_bytes = base64.b64decode(result.pdf)
        ...     with open('output.pdf', 'wb') as f:
        ...         f.write(pdf_bytes)

        Generate a multi-page PDF from multiple layouts:

        >>> layout1 = max.dynamic_layouts.get_dynamic_layout(id="layout-1-id")
        >>> layout2 = max.dynamic_layouts.get_dynamic_layout(id="layout-2-id")
        >>> result = max.dynamic_layouts.generate_pdf_from_layouts(
        ...     layouts=[layout1.layout_json, layout2.layout_json]
        ... )
        >>> if result.success:
        ...     print(f"Generated multi-page PDF")
        ... else:
        ...     print(f"Error: {result.error}")

        Use the PDF directly as an email attachment:

        >>> layout = max.dynamic_layouts.get_dynamic_layout(id="layout-id")
        >>> result = max.dynamic_layouts.generate_pdf_from_layouts(
        ...     layouts=[layout.layout_json]
        ... )
        >>> if result.success:
        ...     email_result = max.email.send_email(
        ...         user_ids=[uuid.UUID("user-id-here")],
        ...         subject="Your Report",
        ...         body="Please see the attached PDF report.",
        ...         attachments=[{
        ...             'filename': 'report.pdf',
        ...             'payload': result.pdf,
        ...             'type': 'application/pdf'
        ...         }]
        ...     )
        """
        mutation_args = {
            'layouts': layouts,
        }

        op = Operations.mutation.generate_pdf_from_layouts
        result = self._gql_client.submit(op, mutation_args)

        return result.generate_pdf_from_layouts
