from __future__ import annotations

from typing import Any, List, Optional
from uuid import UUID

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import (
    TrackedDimensionAttribute,
    TrackedDimensionValuesPage,
)
from answer_rocket.graphql.sdk_operations import Operations


class TrackedValues:
    """
    Helper for reading user-tracked dimension values ("starred" SKUs, brands,
    or other dimension values that users mark from a chat artifact).

    Scoping is enforced server-side:

    * :py:meth:`get_tracked_dimension_values` is **always caller-scoped** — admins
      see only their own stars from this endpoint.
    * :py:meth:`get_all_tracked_dimension_values` is admin-aware — admins see all
      rows across users and datasets; non-admins see only their own.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        self._gql_client = gql_client
        self._config = config

    def get_tracked_dimension_values(
        self, dataset_id: UUID
    ) -> List[TrackedDimensionAttribute]:
        """
        Get currently-active starred values for the calling user on a dataset,
        grouped by dimension.

        Parameters
        ----------
        dataset_id : UUID
            Dataset the starred values belong to.

        Returns
        -------
        List[TrackedDimensionAttribute]
            One entry per dimension the caller has stars in. Each entry exposes
            ``dimension_attribute_id``, ``dimension_name``, and ``values``
            (currently-active starred values for that dimension).

        Examples
        --------
        >>> attrs = max.tracked_values.get_tracked_dimension_values(
        ...     dataset_id=uuid.UUID("...")
        ... )
        >>> for attr in attrs:
        ...     print(attr.dimension_name, attr.values)
        """
        query_args = {"datasetId": str(dataset_id)}
        op = Operations.query.get_tracked_dimension_values
        result = self._gql_client.submit(op, query_args)
        return result.get_tracked_dimension_values

    def get_all_tracked_dimension_values(
        self,
        offset: int = 0,
        limit: int = 100,
        dataset_id: Optional[UUID] = None,
        filters: Optional[dict] = None,
        sort: Optional[list] = None,
    ) -> TrackedDimensionValuesPage:
        """
        Get a flat, paginated view of tracked values. Admins see every user's
        rows; non-admins see only their own.

        Parameters
        ----------
        offset : int, default 0
            Zero-based offset for paging.
        limit : int, default 100
            Max rows to return.
        dataset_id : UUID, optional
            If provided, scope results to a single dataset.
        filters : dict, optional
            AG-Grid filterModel JSON (per-column filters). Keys are column ids
            (e.g. ``"userName"``, ``"value"``, ``"addedUtc"``); values follow
            AG-Grid's text/set/date filter shapes.
        sort : list, optional
            AG-Grid sortModel JSON (list of ``{"colId": ..., "sort": "asc" |
            "desc", "sortIndex": ...}`` entries).

        Returns
        -------
        TrackedDimensionValuesPage
            Object with ``total_count`` (count after filters but before paging)
            and ``rows`` (the requested page of joined user/dataset rows).

        Examples
        --------
        >>> page = max.tracked_values.get_all_tracked_dimension_values(
        ...     dataset_id=uuid.UUID("..."),
        ...     limit=500,
        ... )
        >>> print(page.total_count)
        >>> for row in page.rows:
        ...     print(row.user_name, row.dimension_name, row.value)
        """
        query_args: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "datasetId": str(dataset_id) if dataset_id is not None else None,
            "filters": filters,
            "sort": sort,
        }
        op = Operations.query.get_all_tracked_dimension_values
        result = self._gql_client.submit(op, query_args)
        return result.get_all_tracked_dimension_values
