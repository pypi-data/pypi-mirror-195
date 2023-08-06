from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    PageDtoTranslationPriceListDto,
    PageDtoTranslationPriceSetDto,
    TranslationPriceListCreateDto,
    TranslationPriceListDto,
    TranslationPriceSetBulkDeleteDto,
    TranslationPriceSetBulkMinimumPricesDto,
    TranslationPriceSetBulkPricesDto,
    TranslationPriceSetCreateDto,
    TranslationPriceSetListDto,
)


class PriceListOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getPriceList(
        self, phrase_token: str, priceListUid: str
    ) -> TranslationPriceListDto:
        """
        Get price list

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    async def updatePriceList(
        self, phrase_token: str, priceListUid: str, body: TranslationPriceListCreateDto
    ) -> TranslationPriceListDto:
        """
        Update price list

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param body: TranslationPriceListCreateDto (required), body.

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    async def deletePriceList(self, phrase_token: str, priceListUid: str) -> None:
        """
        Delete price list

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getListOfPriceList(
        self, phrase_token: str, pageNumber: int = "0", pageSize: int = "50"
    ) -> PageDtoTranslationPriceListDto:
        """
        List price lists

        :param phrase_token: string (required) - token to authenticate
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTranslationPriceListDto(**r)

    async def createPriceList(
        self, phrase_token: str, body: TranslationPriceListCreateDto
    ) -> TranslationPriceListDto:
        """
        Create price list

        :param phrase_token: string (required) - token to authenticate
        :param body: TranslationPriceListCreateDto (required), body.

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    async def getPricesWithWorkflowSteps(
        self,
        phrase_token: str,
        priceListUid: str,
        targetLanguages: List[str] = None,
        sourceLanguages: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoTranslationPriceSetDto:
        """
        List price sets

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param targetLanguages: array (optional), query.
        :param sourceLanguages: array (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTranslationPriceSetDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sourceLanguages": sourceLanguages,
            "targetLanguages": targetLanguages,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTranslationPriceSetDto(**r)

    async def createLanguagePair(
        self, phrase_token: str, priceListUid: str, body: TranslationPriceSetCreateDto
    ) -> TranslationPriceSetListDto:
        """
        Add language pairs

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetCreateDto (required), body.

        :return: TranslationPriceSetListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceSetListDto(**r)

    async def deleteLanguagePairs(
        self,
        phrase_token: str,
        priceListUid: str,
        body: TranslationPriceSetBulkDeleteDto,
    ) -> None:
        """
        Remove language pairs

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkDeleteDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def deleteLanguagePair(
        self,
        phrase_token: str,
        targetLanguage: str,
        sourceLanguage: str,
        priceListUid: str,
    ) -> None:
        """
        Remove language pair

        :param phrase_token: string (required) - token to authenticate
        :param targetLanguage: string (required), path.
        :param sourceLanguage: string (required), path.
        :param priceListUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/{sourceLanguage}/{targetLanguage}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def setMinimumPriceForSet(
        self,
        phrase_token: str,
        priceListUid: str,
        body: TranslationPriceSetBulkMinimumPricesDto,
    ) -> TranslationPriceListDto:
        """
        Edit minimum prices

        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkMinimumPricesDto (required), body.

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/minimumPrices"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)

    async def setPrices(
        self,
        phrase_token: str,
        priceListUid: str,
        body: TranslationPriceSetBulkPricesDto,
    ) -> TranslationPriceListDto:
        """
        Edit prices
        If object contains only price, all languages and workflow steps will be updated
        :param phrase_token: string (required) - token to authenticate
        :param priceListUid: string (required), path.
        :param body: TranslationPriceSetBulkPricesDto (required), body.

        :return: TranslationPriceListDto
        """
        endpoint = f"/api2/v1/priceLists/{priceListUid}/priceSets/prices"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TranslationPriceListDto(**r)
