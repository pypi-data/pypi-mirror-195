from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    GlossaryActivationDto,
    GlossaryDto,
    GlossaryEditDto,
    PageDtoGlossaryDto,
)


class GlossaryOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getGlossary(self, phrase_token: str, glossaryUid: str) -> GlossaryDto:
        """
        Get glossary

        :param phrase_token: string (required) - token to authenticate
        :param glossaryUid: string (required), path.

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    async def updateGlossary(
        self, phrase_token: str, glossaryUid: str, body: GlossaryEditDto
    ) -> GlossaryDto:
        """
        Edit glossary
        Languages can only be added, their removal is not supported
        :param phrase_token: string (required) - token to authenticate
        :param glossaryUid: string (required), path.
        :param body: GlossaryEditDto (required), body.

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    async def deleteGlossary(
        self, phrase_token: str, glossaryUid: str, purge: bool = "False"
    ) -> None:
        """
        Delete glossary

        :param phrase_token: string (required) - token to authenticate
        :param glossaryUid: string (required), path.
        :param purge: boolean (optional), query. purge=false - the Glossary can later be restored,
                    &#39;purge=true - the Glossary is completely deleted and cannot be restored.

        :return: None
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def listGlossaries(
        self,
        phrase_token: str,
        lang: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoGlossaryDto:
        """
        List glossaries

        :param phrase_token: string (required) - token to authenticate
        :param lang: array (optional), query. Language of the glossary.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoGlossaryDto
        """
        endpoint = f"/api2/v1/glossaries"
        params = {
            "name": name,
            "lang": lang,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoGlossaryDto(**r)

    async def createGlossary(
        self, phrase_token: str, body: GlossaryEditDto
    ) -> GlossaryDto:
        """
        Create glossary

        :param phrase_token: string (required) - token to authenticate
        :param body: GlossaryEditDto (required), body.

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    async def activateGlossary(
        self, phrase_token: str, glossaryUid: str, body: GlossaryActivationDto
    ) -> GlossaryDto:
        """
        Activate/Deactivate glossary

        :param phrase_token: string (required) - token to authenticate
        :param glossaryUid: string (required), path.
        :param body: GlossaryActivationDto (required), body.

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}/activate"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)
