from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import PageDtoSubDomainDto, SubDomainDto, SubDomainEditDto


class SubdomainOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listSubDomains(
        self,
        phrase_token: str,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoSubDomainDto:
        """
        List subdomains

        :param phrase_token: string (required) - token to authenticate
        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoSubDomainDto
        """
        endpoint = f"/api2/v1/subDomains"
        params = {
            "name": name,
            "createdBy": createdBy,
            "sort": sort,
            "order": order,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoSubDomainDto(**r)

    async def createSubDomain(
        self, phrase_token: str, body: SubDomainEditDto
    ) -> SubDomainDto:
        """
        Create subdomain

        :param phrase_token: string (required) - token to authenticate
        :param body: SubDomainEditDto (required), body.

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    async def getSubDomain(self, phrase_token: str, subDomainUid: str) -> SubDomainDto:
        """
        Get subdomain

        :param phrase_token: string (required) - token to authenticate
        :param subDomainUid: string (required), path.

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    async def updateSubDomain(
        self, phrase_token: str, subDomainUid: str, body: SubDomainEditDto
    ) -> SubDomainDto:
        """
        Edit subdomain

        :param phrase_token: string (required) - token to authenticate
        :param subDomainUid: string (required), path.
        :param body: SubDomainEditDto (required), body.

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    async def deleteSubDomain(self, phrase_token: str, subDomainUid: str) -> None:
        """
        Delete subdomain

        :param phrase_token: string (required) - token to authenticate
        :param subDomainUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return
