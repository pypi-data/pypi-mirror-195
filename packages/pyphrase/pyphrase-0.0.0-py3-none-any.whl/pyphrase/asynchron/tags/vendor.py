from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import CreateVendorDto, PageDtoVendorDto, VendorDto


class VendorOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getVendor(self, phrase_token: str, vendorUid: str) -> VendorDto:
        """
        Get vendor

        :param phrase_token: string (required) - token to authenticate
        :param vendorUid: string (required), path.

        :return: VendorDto
        """
        endpoint = f"/api2/v1/vendors/{vendorUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return VendorDto(**r)

    async def listVendors(
        self,
        phrase_token: str,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoVendorDto:
        """
        List vendors

        :param phrase_token: string (required) - token to authenticate
        :param name: string (optional), query. Name or the vendor, for filtering.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoVendorDto
        """
        endpoint = f"/api2/v1/vendors"
        params = {"pageNumber": pageNumber, "pageSize": pageSize, "name": name}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoVendorDto(**r)

    async def createVendor(self, phrase_token: str, body: CreateVendorDto) -> VendorDto:
        """
        Create vendor

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateVendorDto (required), body.

        :return: VendorDto
        """
        endpoint = f"/api2/v1/vendors"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return VendorDto(**r)
