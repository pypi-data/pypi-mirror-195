from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    MachineTranslateSettingsPbmDto,
    MachineTranslateStatusDto,
    PageDtoMachineTranslateSettingsPbmDto,
    TypesDto,
)


class MachineTranslationSettingsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getStatus(
        self, phrase_token: str, mtsUid: str
    ) -> MachineTranslateStatusDto:
        """
        Get status of machine translate engine

        :param phrase_token: string (required) - token to authenticate
        :param mtsUid: string (required), path.

        :return: MachineTranslateStatusDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings/{mtsUid}/status"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MachineTranslateStatusDto(**r)

    async def getMTSettings(
        self, phrase_token: str, mtsUid: str
    ) -> MachineTranslateSettingsPbmDto:
        """
        Get machine translate settings

        :param phrase_token: string (required) - token to authenticate
        :param mtsUid: string (required), path.

        :return: MachineTranslateSettingsPbmDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings/{mtsUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MachineTranslateSettingsPbmDto(**r)

    async def getList(
        self,
        phrase_token: str,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoMachineTranslateSettingsPbmDto:
        """
        List machine translate settings

        :param phrase_token: string (required) - token to authenticate
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoMachineTranslateSettingsPbmDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings"
        params = {"name": name, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoMachineTranslateSettingsPbmDto(**r)

    async def getMTTypes(
        self,
        phrase_token: str,
    ) -> TypesDto:
        """
        Get machine translate settings types

        :param phrase_token: string (required) - token to authenticate

        :return: TypesDto
        """
        endpoint = f"/api2/v1/machineTranslateSettings/types"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TypesDto(**r)
