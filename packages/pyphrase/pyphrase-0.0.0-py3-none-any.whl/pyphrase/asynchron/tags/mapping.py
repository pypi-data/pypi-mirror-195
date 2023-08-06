from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import TaskMappingDto


class MappingOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getMappingForTask(
        self, phrase_token: str, id: str, workflowLevel: int = "1"
    ) -> TaskMappingDto:
        """
        Returns mapping for taskId (mxliff)

        :param phrase_token: string (required) - token to authenticate
        :param id: string (required), path.
        :param workflowLevel: integer (optional), query.

        :return: TaskMappingDto
        """
        endpoint = f"/api2/v1/mappings/tasks/{id}"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TaskMappingDto(**r)
