from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import LanguageListDto


class SupportedLanguagesOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listOfLanguages(
        self,
        phrase_token: str,
    ) -> LanguageListDto:
        """
        List supported languages

        :param phrase_token: string (required) - token to authenticate

        :return: LanguageListDto
        """
        endpoint = f"/api2/v1/languages"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LanguageListDto(**r)
