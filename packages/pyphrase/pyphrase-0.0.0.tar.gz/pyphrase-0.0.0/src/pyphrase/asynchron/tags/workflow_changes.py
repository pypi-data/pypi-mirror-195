from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import Response, WorkflowChangesDto


class WorkflowChangesOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def downloadWorkflowChanges(
        self, phrase_token: str, body: WorkflowChangesDto
    ) -> Response:
        """
        Download workflow changes report

        :param phrase_token: string (required) - token to authenticate
        :param body: WorkflowChangesDto (required), body.

        :return: Response
        """
        endpoint = f"/api2/v2/jobs/workflowChanges"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return Response(**r)
