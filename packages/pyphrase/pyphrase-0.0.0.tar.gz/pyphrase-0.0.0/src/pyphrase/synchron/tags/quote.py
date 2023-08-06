from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    EmailQuotesRequestDto,
    EmailQuotesResponseDto,
    QuoteCreateV2Dto,
    QuoteDto,
    QuoteV2Dto,
)


class QuoteOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def get_2(self, phrase_token: str, quoteUid: str) -> QuoteDto:
        """
        Get quote

        :param phrase_token: string (required) - token to authenticate
        :param quoteUid: string (required), path.

        :return: QuoteDto
        """
        endpoint = f"/api2/v1/quotes/{quoteUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QuoteDto(**r)

    def deleteQuote(self, phrase_token: str, quoteUid: str) -> None:
        """
        Delete quote

        :param phrase_token: string (required) - token to authenticate
        :param quoteUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/quotes/{quoteUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def emailQuotes(
        self, phrase_token: str, body: EmailQuotesRequestDto
    ) -> EmailQuotesResponseDto:
        """
        Email quotes

        :param phrase_token: string (required) - token to authenticate
        :param body: EmailQuotesRequestDto (required), body.

        :return: EmailQuotesResponseDto
        """
        endpoint = f"/api2/v1/quotes/email"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return EmailQuotesResponseDto(**r)

    def createQuoteV2(self, phrase_token: str, body: QuoteCreateV2Dto) -> QuoteV2Dto:
        """
        Create quote
        Either WorkflowSettings or Units must be sent for billingUnit "Hour".
        :param phrase_token: string (required) - token to authenticate
        :param body: QuoteCreateV2Dto (required), body.

        :return: QuoteV2Dto
        """
        endpoint = f"/api2/v2/quotes"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QuoteV2Dto(**r)
