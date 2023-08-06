from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ScimResourceSchema,
    ScimResourceTypeSchema,
    ScimUserCoreDto,
    ServiceProviderConfigDto,
)


class ScimOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getSchemas(
        self,
        phrase_token: str,
    ) -> ScimResourceSchema:
        """
        Get supported SCIM Schemas

        :param phrase_token: string (required) - token to authenticate

        :return: ScimResourceSchema
        """
        endpoint = f"/api2/v1/scim/Schemas"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimResourceSchema(**r)

    async def getSchemaByUrn(
        self, phrase_token: str, schemaUrn: str
    ) -> ScimResourceSchema:
        """
        Get supported SCIM Schema by urn

        :param phrase_token: string (required) - token to authenticate
        :param schemaUrn: string (required), path.

        :return: ScimResourceSchema
        """
        endpoint = f"/api2/v1/scim/Schemas/{schemaUrn}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimResourceSchema(**r)

    async def getServiceProviderConfigDto(
        self,
        phrase_token: str,
    ) -> ServiceProviderConfigDto:
        """
        Retrieve the Service Provider's Configuration

        :param phrase_token: string (required) - token to authenticate

        :return: ServiceProviderConfigDto
        """
        endpoint = f"/api2/v1/scim/ServiceProviderConfig"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ServiceProviderConfigDto(**r)

    async def getResourceTypes(
        self,
        phrase_token: str,
    ) -> ScimResourceTypeSchema:
        """
        List the types of SCIM Resources available

        :param phrase_token: string (required) - token to authenticate

        :return: ScimResourceTypeSchema
        """
        endpoint = f"/api2/v1/scim/ResourceTypes"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimResourceTypeSchema(**r)

    async def getScimUser(self, phrase_token: str, userId: int) -> ScimUserCoreDto:
        """
        Get user

        :param phrase_token: string (required) - token to authenticate
        :param userId: integer (required), path.

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def editUser(
        self, phrase_token: str, userId: int, body: ScimUserCoreDto
    ) -> ScimUserCoreDto:
        """
        Edit user using SCIM

        :param phrase_token: string (required) - token to authenticate
        :param userId: integer (required), path.
        :param body: ScimUserCoreDto (required), body.

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def deleteUser(self, phrase_token: str, userId: int) -> None:
        """
        Delete user using SCIM

        :param phrase_token: string (required) - token to authenticate
        :param userId: integer (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def patchUser(
        self, phrase_token: str, userId: int, body: Any
    ) -> ScimUserCoreDto:
        """
        Patch user using SCIM

        :param phrase_token: string (required) - token to authenticate
        :param userId: integer (required), path.
        :param body: Any (required), body.

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def searchUsers(
        self,
        phrase_token: str,
        sortBy: str = None,
        attributes: str = None,
        filter: str = None,
        sortOrder: str = "ascending",
        startIndex: int = "1",
        count: int = "50",
    ) -> Any:
        """
                Search users
                This operation supports <a href="http://ldapwiki.com/wiki/SCIM%20Filtering" target="_blank">SCIM Filter</a>,
        <a href="http://ldapwiki.com/wiki/SCIM%20Search%20Request" target="_blank">SCIM attributes</a> and
        <a href="http://ldapwiki.com/wiki/SCIM%20Sorting" target="_blank">SCIM sort</a>

        Supported attributes:
          - `id`
          - `active`
          - `userName`
          - `name.givenName`
          - `name.familyName`
          - `emails.value`
          - `meta.created`
                :param phrase_token: string (required) - token to authenticate
                :param sortBy: string (optional), query. See method description.
                :param attributes: string (optional), query. See method description.
                :param filter: string (optional), query. See method description.
                :param sortOrder: string (optional), query. See method description.
                :param startIndex: integer (optional), query. The 1-based index of the first search result. Default 1.
                :param count: integer (optional), query. Non-negative Integer. Specifies the desired maximum number of search results per page; e.g., 10..

                :return:
        """
        endpoint = f"/api2/v1/scim/Users"
        params = {
            "filter": filter,
            "attributes": attributes,
            "sortBy": sortBy,
            "sortOrder": sortOrder,
            "startIndex": startIndex,
            "count": count,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def createUserSCIM(
        self, phrase_token: str, body: ScimUserCoreDto
    ) -> ScimUserCoreDto:
        """
                Create user using SCIM
                Supported schema: `"urn:ietf:params:scim:schemas:core:2.0:User"`

        Create active user:
        ```
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User"
            ],
            "active": true,
            "userName": "john.doe",
            "emails": [
                {
                    "primary": true,
                    "value": "john.doe@example.com",
                    "type": "work"
                }
            ],
            "name": {
                "givenName": "John",
                "familyName": "Doe"
            }
        }
        ```
                :param phrase_token: string (required) - token to authenticate
                :param body: ScimUserCoreDto (required), body.

                :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)
