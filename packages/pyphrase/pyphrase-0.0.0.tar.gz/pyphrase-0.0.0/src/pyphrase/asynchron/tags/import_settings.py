from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ImportSettingsCreateDto,
    ImportSettingsDto,
    ImportSettingsEditDto,
    PageDtoImportSettingsReference,
)


class ImportSettingsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getImportSettings(
        self,
        phrase_token: str,
    ) -> ImportSettingsDto:
        """
        Get organization's default import settings

        :param phrase_token: string (required) - token to authenticate

        :return: ImportSettingsDto
        """
        endpoint = f"/api2/v1/importSettings/default"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def getImportSettings_1(
        self, phrase_token: str, uid: str
    ) -> ImportSettingsDto:
        """
        Get import settings

        :param phrase_token: string (required) - token to authenticate
        :param uid: string (required), path.

        :return: ImportSettingsDto
        """
        endpoint = f"/api2/v1/importSettings/{uid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def deleteImportSettings(self, phrase_token: str, uid: str) -> None:
        """
        Delete import settings

        :param phrase_token: string (required) - token to authenticate
        :param uid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/importSettings/{uid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def listImportSettings(
        self,
        phrase_token: str,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoImportSettingsReference:
        """
        List import settings

        :param phrase_token: string (required) - token to authenticate
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoImportSettingsReference
        """
        endpoint = f"/api2/v1/importSettings"
        params = {"name": name, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoImportSettingsReference(**r)

    async def createImportSettings(
        self, phrase_token: str, body: ImportSettingsCreateDto
    ) -> ImportSettingsDto:
        """
        Create import settings
        Pre-defined import settings is handy for [Create Job](#operation/createJob).
                  See [supported file types](https://wiki.memsource.com/wiki/API_File_Type_List)
        :param phrase_token: string (required) - token to authenticate
        :param body: ImportSettingsCreateDto (required), body.

        :return: ImportSettingsDto
        """
        endpoint = f"/api2/v1/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)

    async def editImportSettings(
        self, phrase_token: str, body: ImportSettingsEditDto
    ) -> ImportSettingsDto:
        """
        Edit import settings

        :param phrase_token: string (required) - token to authenticate
        :param body: ImportSettingsEditDto (required), body.

        :return: ImportSettingsDto
        """
        endpoint = f"/api2/v1/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ImportSettingsDto(**r)
