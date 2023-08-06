from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    DictionaryItemDto,
    SpellCheckRequestDto,
    SpellCheckResponseDto,
    SuggestRequestDto,
    SuggestResponseDto,
)


class SpellCheckOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def check(
        self, phrase_token: str, body: SpellCheckRequestDto
    ) -> SpellCheckResponseDto:
        """
        Spell check
        Spell check using the settings of the user's organization
        :param phrase_token: string (required) - token to authenticate
        :param body: SpellCheckRequestDto (required), body.

        :return: SpellCheckResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/check"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SpellCheckResponseDto(**r)

    def checkByJob(
        self, phrase_token: str, jobUid: str, body: SpellCheckRequestDto
    ) -> SpellCheckResponseDto:
        """
        Spell check for job
        Spell check using the settings from the project of the job
        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param body: SpellCheckRequestDto (required), body.

        :return: SpellCheckResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/check/{jobUid}"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SpellCheckResponseDto(**r)

    def addWord(self, phrase_token: str, body: DictionaryItemDto) -> None:
        """
        Add word to dictionary

        :param phrase_token: string (required) - token to authenticate
        :param body: DictionaryItemDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/spellCheck/words"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def suggest(self, phrase_token: str, body: SuggestRequestDto) -> SuggestResponseDto:
        """
        Suggest a word
        Spell check suggest using the users's spell check dictionary
        :param phrase_token: string (required) - token to authenticate
        :param body: SuggestRequestDto (required), body.

        :return: SuggestResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/suggest"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SuggestResponseDto(**r)
