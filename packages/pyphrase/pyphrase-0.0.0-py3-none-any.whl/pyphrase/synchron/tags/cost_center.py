from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CostCenterDto,
    CostCenterEditDto,
    PageDtoCostCenterDto,
)


class CostCenterOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getCostCenter(self, phrase_token: str, costCenterUid: str) -> CostCenterDto:
        """
        Get cost center

        :param phrase_token: string (required) - token to authenticate
        :param costCenterUid: string (required), path.

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)

    def updateCostCenter(
        self, phrase_token: str, costCenterUid: str, body: CostCenterEditDto
    ) -> CostCenterDto:
        """
        Edit cost center

        :param phrase_token: string (required) - token to authenticate
        :param costCenterUid: string (required), path.
        :param body: CostCenterEditDto (required), body.

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)

    def deleteCostCenter(self, phrase_token: str, costCenterUid: str) -> None:
        """
        Delete cost center

        :param phrase_token: string (required) - token to authenticate
        :param costCenterUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listCostCenters(
        self,
        phrase_token: str,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoCostCenterDto:
        """
        List of cost centers

        :param phrase_token: string (required) - token to authenticate
        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoCostCenterDto
        """
        endpoint = f"/api2/v1/costCenters"
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

        return PageDtoCostCenterDto(**r)

    def createCostCenter(
        self, phrase_token: str, body: CostCenterEditDto
    ) -> CostCenterDto:
        """
        Create cost center

        :param phrase_token: string (required) - token to authenticate
        :param body: CostCenterEditDto (required), body.

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)
