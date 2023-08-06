from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AdditionalWorkflowStepDto,
    AdditionalWorkflowStepRequestDto,
    PageDtoAdditionalWorkflowStepDto,
)


class AdditionalWorkflowStepOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def deleteAWFStep(self, phrase_token: str, id: str) -> None:
        """
        Delete additional workflow step

        :param phrase_token: string (required) - token to authenticate
        :param id: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps/{id}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def listAWFSteps(
        self,
        phrase_token: str,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoAdditionalWorkflowStepDto:
        """
        List additional workflow steps

        :param phrase_token: string (required) - token to authenticate
        :param name: string (optional), query. Name of the additional workflow step to filter.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoAdditionalWorkflowStepDto
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps"
        params = {"pageNumber": pageNumber, "pageSize": pageSize, "name": name}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAdditionalWorkflowStepDto(**r)

    async def createAWFStep(
        self, phrase_token: str, body: AdditionalWorkflowStepRequestDto
    ) -> AdditionalWorkflowStepDto:
        """
        Create additional workflow step

        :param phrase_token: string (required) - token to authenticate
        :param body: AdditionalWorkflowStepRequestDto (required), body.

        :return: AdditionalWorkflowStepDto
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AdditionalWorkflowStepDto(**r)
