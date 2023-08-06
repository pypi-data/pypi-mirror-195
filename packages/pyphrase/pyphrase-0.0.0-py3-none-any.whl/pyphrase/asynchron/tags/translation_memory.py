from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AsyncExportTMByQueryResponseDto,
    AsyncExportTMResponseDto,
    AsyncRequestWrapperDto,
    AsyncRequestWrapperV2Dto,
    BackgroundTasksTmDto,
    CleanedTransMemoriesDto,
    ExportByQueryDto,
    ExportTMDto,
    InputStream,
    MetadataResponse,
    PageDtoAbstractProjectDto,
    PageDtoTransMemoryDto,
    SearchRequestDto,
    SearchResponseListTmDto,
    SearchTMByJobRequestDto,
    SegmentDto,
    TargetLanguageDto,
    TranslationDto,
    TransMemoryCreateDto,
    TransMemoryDto,
    TransMemoryEditDto,
    WildCardSearchRequestDto,
)


class TranslationMemoryOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def searchSegmentByJob(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        body: SearchTMByJobRequestDto,
    ) -> SearchResponseListTmDto:
        """
        Search translation memory for segment by job
        Returns at most <i>maxSegments</i>
            records with <i>score >= scoreThreshold</i> and at most <i>maxSubsegments</i> records which are subsegment,
            i.e. the source text is substring of the query text.
        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: SearchTMByJobRequestDto (required), body.

        :return: SearchResponseListTmDto
        """
        endpoint = (
            f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/transMemories/searchSegment"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    async def search(
        self, phrase_token: str, transMemoryUid: str, body: SearchRequestDto
    ) -> SearchResponseListTmDto:
        """
        Search translation memory (sync)

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: SearchRequestDto (required), body.

        :return: SearchResponseListTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/search"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    async def listTransMemories(
        self,
        phrase_token: str,
        businessUnitId: str = None,
        subDomainId: str = None,
        domainId: str = None,
        clientId: str = None,
        targetLang: str = None,
        sourceLang: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoTransMemoryDto:
        """
        List translation memories

        :param phrase_token: string (required) - token to authenticate
        :param businessUnitId: string (optional), query.
        :param subDomainId: string (optional), query.
        :param domainId: string (optional), query.
        :param clientId: string (optional), query.
        :param targetLang: string (optional), query.
        :param sourceLang: string (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories"
        params = {
            "name": name,
            "sourceLang": sourceLang,
            "targetLang": targetLang,
            "clientId": clientId,
            "domainId": domainId,
            "subDomainId": subDomainId,
            "businessUnitId": businessUnitId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    async def createTransMemory(
        self, phrase_token: str, body: TransMemoryCreateDto
    ) -> TransMemoryDto:
        """
        Create translation memory

        :param phrase_token: string (required) - token to authenticate
        :param body: TransMemoryCreateDto (required), body.

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    async def exportCleanedTMs(
        self, phrase_token: str, body: CleanedTransMemoriesDto
    ) -> AsyncRequestWrapperDto:
        """
        Extract cleaned translation memory
        Returns a ZIP file containing the cleaned translation memories in the specified outputFormat.
        :param phrase_token: string (required) - token to authenticate
        :param body: CleanedTransMemoriesDto (required), body.

        :return: AsyncRequestWrapperDto
        """
        endpoint = f"/api2/v1/transMemories/extractCleaned"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperDto(**r)

    async def getTransMemory(
        self, phrase_token: str, transMemoryUid: str
    ) -> TransMemoryDto:
        """
        Get translation memory

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    async def editTransMemory(
        self, phrase_token: str, transMemoryUid: str, body: TransMemoryEditDto
    ) -> TransMemoryDto:
        """
        Edit translation memory

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: TransMemoryEditDto (required), body.

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    async def deleteTransMemory(
        self, phrase_token: str, transMemoryUid: str, purge: bool = "False"
    ) -> None:
        """
        Delete translation memory

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param purge: boolean (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def addTargetLangToTransMemory(
        self, phrase_token: str, transMemoryUid: str, body: TargetLanguageDto
    ) -> TransMemoryDto:
        """
        Add target language to translation memory

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: TargetLanguageDto (required), body.

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/targetLanguages"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    async def downloadCleanedTM(self, phrase_token: str, asyncRequestId: str) -> bytes:
        """
        Download cleaned TM

        :param phrase_token: string (required) - token to authenticate
        :param asyncRequestId: string (required), path. Request ID.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/downloadCleaned/{asyncRequestId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def insertToTransMemory(
        self, phrase_token: str, transMemoryUid: str, body: SegmentDto
    ) -> None:
        """
        Insert segment

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: SegmentDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def clearTransMemory(self, phrase_token: str, transMemoryUid: str) -> None:
        """
        Delete all segments

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getRelatedProjects(
        self,
        phrase_token: str,
        transMemoryUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoAbstractProjectDto:
        """
        List related projects

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoAbstractProjectDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/relatedProjects"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAbstractProjectDto(**r)

    async def getMetadata(
        self, phrase_token: str, transMemoryUid: str, byLanguage: bool = "False"
    ) -> MetadataResponse:
        """
        Get translation memory metadata

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param byLanguage: boolean (optional), query.

        :return: MetadataResponse
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/metadata"
        params = {"byLanguage": byLanguage}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MetadataResponse(**r)

    async def updateTranslation(
        self,
        phrase_token: str,
        segmentId: str,
        transMemoryUid: str,
        body: TranslationDto,
    ) -> None:
        """
        Edit segment

        :param phrase_token: string (required) - token to authenticate
        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.
        :param body: TranslationDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def deleteSourceAndTranslations(
        self, phrase_token: str, segmentId: str, transMemoryUid: str
    ) -> None:
        """
        Delete both source and translation
        Not recommended for bulk removal of segments
        :param phrase_token: string (required) - token to authenticate
        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def deleteTranslation(
        self, phrase_token: str, lang: str, segmentId: str, transMemoryUid: str
    ) -> None:
        """
        Delete segment of given language
        Not recommended for bulk removal of segments
        :param phrase_token: string (required) - token to authenticate
        :param lang: string (required), path.
        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.

        :return: None
        """
        endpoint = (
            f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}/lang/{lang}"
        )
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getBackgroundTasks_1(
        self, phrase_token: str, transMemoryUid: str
    ) -> BackgroundTasksTmDto:
        """
        Get last task information

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.

        :return: BackgroundTasksTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/lastBackgroundTask"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BackgroundTasksTmDto(**r)

    async def wildcardSearch(
        self, phrase_token: str, transMemoryUid: str, body: WildCardSearchRequestDto
    ) -> SearchResponseListTmDto:
        """
        Wildcard search

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: WildCardSearchRequestDto (required), body.

        :return: SearchResponseListTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/wildCardSearch"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    async def downloadSearchResult(
        self,
        phrase_token: str,
        asyncRequestId: str,
        fields: List[str] = None,
        format: str = "TMX",
    ) -> bytes:
        """
        Download export

        :param phrase_token: string (required) - token to authenticate
        :param asyncRequestId: string (required), path. Request ID.
        :param fields: array (optional), query. Fields to include in exported XLSX.
        :param format: string (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/downloadExport/{asyncRequestId}"
        params = {"format": format, "fields": fields}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def exportByQueryAsync(
        self, phrase_token: str, transMemoryUid: str, body: ExportByQueryDto
    ) -> AsyncExportTMByQueryResponseDto:
        """
        Search translation memory
        Use [this API](#operation/downloadSearchResult) to download result
        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: ExportByQueryDto (required), body.

        :return: AsyncExportTMByQueryResponseDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/exportByQueryAsync"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncExportTMByQueryResponseDto(**r)

    async def clearTransMemoryV2(self, phrase_token: str, transMemoryUid: str) -> None:
        """
        Delete all segments.
        This call is **asynchronous**, use [this API](#operation/getAsyncRequest) to check the result
        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def importTransMemoryV2(
        self,
        phrase_token: str,
        transMemoryUid: str,
        body: InputStream,
        strictLangMatching: bool = "False",
        stripNativeCodes: bool = "True",
    ) -> AsyncRequestWrapperV2Dto:
        """
        Import TMX

        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: InputStream (required), body.
        :param strictLangMatching: boolean (optional), query.
        :param stripNativeCodes: boolean (optional), query.

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/import"
        params = {
            "strictLangMatching": strictLangMatching,
            "stripNativeCodes": stripNativeCodes,
        }

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)

    async def exportV2(
        self, phrase_token: str, transMemoryUid: str, body: ExportTMDto
    ) -> AsyncExportTMResponseDto:
        """
        Export translation memory
        Use [this API](#operation/downloadSearchResult) to download result
        :param phrase_token: string (required) - token to authenticate
        :param transMemoryUid: string (required), path.
        :param body: ExportTMDto (required), body.

        :return: AsyncExportTMResponseDto
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/export"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncExportTMResponseDto(**r)
