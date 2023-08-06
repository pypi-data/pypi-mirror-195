from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    BusinessUnitDto,
    BusinessUnitEditDto,
    PageDtoBusinessUnitDto,
)


class BusinessUnitOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getBusinessUnit(
        self, phrase_token: str, businessUnitUid: str
    ) -> BusinessUnitDto:
        """
        Get business unit

        :param phrase_token: string (required) - token to authenticate
        :param businessUnitUid: string (required), path.

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)

    def updateBusinessUnit(
        self, phrase_token: str, businessUnitUid: str, body: BusinessUnitEditDto
    ) -> BusinessUnitDto:
        """
        Edit business unit

        :param phrase_token: string (required) - token to authenticate
        :param businessUnitUid: string (required), path.
        :param body: BusinessUnitEditDto (required), body.

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)

    def deleteBusinessUnit(self, phrase_token: str, businessUnitUid: str) -> None:
        """
        Delete business unit

        :param phrase_token: string (required) - token to authenticate
        :param businessUnitUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listBusinessUnits(
        self,
        phrase_token: str,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoBusinessUnitDto:
        """
        List business units

        :param phrase_token: string (required) - token to authenticate
        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query. Unique name of the business unit.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoBusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits"
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

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoBusinessUnitDto(**r)

    def createBusinessUnit(
        self, phrase_token: str, body: BusinessUnitEditDto
    ) -> BusinessUnitDto:
        """
        Create business unit

        :param phrase_token: string (required) - token to authenticate
        :param body: BusinessUnitEditDto (required), body.

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)
