from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import ClientDto, ClientEditDto, PageDtoClientDto


class ClientOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getClient(self, phrase_token: str, clientUid: str) -> ClientDto:
        """
        Get client

        :param phrase_token: string (required) - token to authenticate
        :param clientUid: string (required), path.

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ClientDto(**r)

    async def updateClient(
        self, phrase_token: str, clientUid: str, body: ClientEditDto
    ) -> ClientDto:
        """
        Edit client

        :param phrase_token: string (required) - token to authenticate
        :param clientUid: string (required), path.
        :param body: ClientEditDto (required), body.

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ClientDto(**r)

    async def deleteClient(self, phrase_token: str, clientUid: str) -> None:
        """
        Delete client

        :param phrase_token: string (required) - token to authenticate
        :param clientUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def listClients(
        self,
        phrase_token: str,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoClientDto:
        """
        List clients

        :param phrase_token: string (required) - token to authenticate
        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query. Unique name of the Client.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoClientDto
        """
        endpoint = f"/api2/v1/clients"
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

        return PageDtoClientDto(**r)

    async def createClient(self, phrase_token: str, body: ClientEditDto) -> ClientDto:
        """
        Create client

        :param phrase_token: string (required) - token to authenticate
        :param body: ClientEditDto (required), body.

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ClientDto(**r)
