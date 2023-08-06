from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateCustomFileTypeDto,
    CustomFileTypeDto,
    DeleteCustomFileTypeDto,
    PageDtoCustomFileTypeDto,
    UpdateCustomFileTypeDto,
)


class CustomFileTypeOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getAllCustomFileType(
        self, phrase_token: str, pageNumber: int = "0", pageSize: int = "50"
    ) -> PageDtoCustomFileTypeDto:
        """
        Get All Custom file type

        :param phrase_token: string (required) - token to authenticate
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoCustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoCustomFileTypeDto(**r)

    async def createCustomFileTypes(
        self, phrase_token: str, body: CreateCustomFileTypeDto
    ) -> CustomFileTypeDto:
        """
        Create custom file type

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateCustomFileTypeDto (required), body.

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def deleteBatchCustomFileType(
        self, phrase_token: str, body: DeleteCustomFileTypeDto
    ) -> None:
        """
        Delete multiple Custom file type

        :param phrase_token: string (required) - token to authenticate
        :param body: DeleteCustomFileTypeDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getCustomFileType(
        self, phrase_token: str, customFileTypeUid: str
    ) -> CustomFileTypeDto:
        """
        Get Custom file type

        :param phrase_token: string (required) - token to authenticate
        :param customFileTypeUid: string (required), path.

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def updateCustomFileType(
        self, phrase_token: str, customFileTypeUid: str, body: UpdateCustomFileTypeDto
    ) -> CustomFileTypeDto:
        """
        Update Custom file type

        :param phrase_token: string (required) - token to authenticate
        :param customFileTypeUid: string (required), path.
        :param body: UpdateCustomFileTypeDto (required), body.

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def deleteCustomFileType(
        self, phrase_token: str, customFileTypeUid: str
    ) -> None:
        """
        Delete Custom file type

        :param phrase_token: string (required) - token to authenticate
        :param customFileTypeUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return
