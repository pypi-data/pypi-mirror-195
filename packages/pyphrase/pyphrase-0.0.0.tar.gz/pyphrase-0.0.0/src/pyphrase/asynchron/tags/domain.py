from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import DomainDto, DomainEditDto, PageDtoDomainDto


class DomainOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getDomain(self, phrase_token: str, domainUid: str) -> DomainDto:
        """
        Get domain

        :param phrase_token: string (required) - token to authenticate
        :param domainUid: string (required), path.

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return DomainDto(**r)

    async def updateDomain(
        self, phrase_token: str, domainUid: str, body: DomainEditDto
    ) -> DomainDto:
        """
        Edit domain

        :param phrase_token: string (required) - token to authenticate
        :param domainUid: string (required), path.
        :param body: DomainEditDto (required), body.

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return DomainDto(**r)

    async def deleteDomain(self, phrase_token: str, domainUid: str) -> None:
        """
        Delete domain

        :param phrase_token: string (required) - token to authenticate
        :param domainUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def listDomains(
        self,
        phrase_token: str,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoDomainDto:
        """
        List of domains

        :param phrase_token: string (required) - token to authenticate
        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoDomainDto
        """
        endpoint = f"/api2/v1/domains"
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

        return PageDtoDomainDto(**r)

    async def createDomain(self, phrase_token: str, body: DomainEditDto) -> DomainDto:
        """
        Create domain

        :param phrase_token: string (required) - token to authenticate
        :param body: DomainEditDto (required), body.

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return DomainDto(**r)
