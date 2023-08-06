from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    DiscountSchemeCreateDto,
    NetRateScheme,
    NetRateSchemeEdit,
    NetRateSchemeWorkflowStep,
    NetRateSchemeWorkflowStepEdit,
    PageDtoNetRateSchemeReference,
    PageDtoNetRateSchemeWorkflowStepReference,
)


class NetRateSchemeOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getDiscountScheme(
        self, phrase_token: str, netRateSchemeUid: str
    ) -> NetRateScheme:
        """
        Get net rate scheme

        :param phrase_token: string (required) - token to authenticate
        :param netRateSchemeUid: string (required), path.

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    async def updateDiscountScheme(
        self, phrase_token: str, netRateSchemeUid: str, body: NetRateSchemeEdit
    ) -> NetRateScheme:
        """
        Edit net rate scheme

        :param phrase_token: string (required) - token to authenticate
        :param netRateSchemeUid: string (required), path.
        :param body: NetRateSchemeEdit (required), body.

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    async def getDiscountSchemes(
        self, phrase_token: str, pageNumber: int = "0", pageSize: int = "50"
    ) -> PageDtoNetRateSchemeReference:
        """
        List net rate schemes

        :param phrase_token: string (required) - token to authenticate
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoNetRateSchemeReference
        """
        endpoint = f"/api2/v1/netRateSchemes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoNetRateSchemeReference(**r)

    async def createDiscountScheme(
        self, phrase_token: str, body: DiscountSchemeCreateDto
    ) -> NetRateScheme:
        """
        Create net rate scheme

        :param phrase_token: string (required) - token to authenticate
        :param body: DiscountSchemeCreateDto (required), body.

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    async def getDiscountSchemeWorkflowStep(
        self, phrase_token: str, netRateSchemeWorkflowStepId: int, netRateSchemeUid: str
    ) -> NetRateSchemeWorkflowStep:
        """
        Get scheme for workflow step

        :param phrase_token: string (required) - token to authenticate
        :param netRateSchemeWorkflowStepId: integer (required), path.
        :param netRateSchemeUid: string (required), path.

        :return: NetRateSchemeWorkflowStep
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes/{netRateSchemeWorkflowStepId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return NetRateSchemeWorkflowStep(**r)

    async def editDiscountSchemeWorkflowStep(
        self,
        phrase_token: str,
        netRateSchemeWorkflowStepId: int,
        netRateSchemeUid: str,
        body: NetRateSchemeWorkflowStepEdit,
    ) -> NetRateSchemeWorkflowStep:
        """
        Edit scheme for workflow step

        :param phrase_token: string (required) - token to authenticate
        :param netRateSchemeWorkflowStepId: integer (required), path.
        :param netRateSchemeUid: string (required), path.
        :param body: NetRateSchemeWorkflowStepEdit (required), body.

        :return: NetRateSchemeWorkflowStep
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes/{netRateSchemeWorkflowStepId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return NetRateSchemeWorkflowStep(**r)

    async def getDiscountSchemeWorkflowSteps(
        self,
        phrase_token: str,
        netRateSchemeUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoNetRateSchemeWorkflowStepReference:
        """
        List schemes for workflow step

        :param phrase_token: string (required) - token to authenticate
        :param netRateSchemeUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoNetRateSchemeWorkflowStepReference
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoNetRateSchemeWorkflowStepReference(**r)
