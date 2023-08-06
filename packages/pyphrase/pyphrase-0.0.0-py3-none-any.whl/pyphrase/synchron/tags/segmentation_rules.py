from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    EditSegmentationRuleDto,
    InputStream,
    PageDtoSegmentationRuleReference,
    SegmentationRuleDto,
)


class SegmentationRulesOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getListOfSegmentationRules(
        self,
        phrase_token: str,
        locales: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoSegmentationRuleReference:
        """
        List segmentation rules

        :param phrase_token: string (required) - token to authenticate
        :param locales: array (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoSegmentationRuleReference
        """
        endpoint = f"/api2/v1/segmentationRules"
        params = {"locales": locales, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoSegmentationRuleReference(**r)

    def createSegmentationRule(
        self, phrase_token: str, body: InputStream
    ) -> SegmentationRuleDto:
        """
        Create segmentation rule
        Creates new Segmentation Rule with file and segRule JSON Object as header parameter. The same object is used for GET action.
        :param phrase_token: string (required) - token to authenticate
        :param body: InputStream (required), body. streamed file.

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    def getSegmentationRule(
        self, phrase_token: str, segRuleId: int
    ) -> SegmentationRuleDto:
        """
        Get segmentation rule

        :param phrase_token: string (required) - token to authenticate
        :param segRuleId: integer (required), path.

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    def updatesSegmentationRule(
        self, phrase_token: str, segRuleId: int, body: EditSegmentationRuleDto
    ) -> SegmentationRuleDto:
        """
        Edit segmentation rule

        :param phrase_token: string (required) - token to authenticate
        :param segRuleId: integer (required), path.
        :param body: EditSegmentationRuleDto (required), body.

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    def deletesSegmentationRule(self, phrase_token: str, segRuleId: int) -> None:
        """
        Delete segmentation rule

        :param phrase_token: string (required) - token to authenticate
        :param segRuleId: integer (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return
