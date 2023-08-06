from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AnalyseJobDto,
    AnalyseLanguagePartDto,
    AnalyseRecalculateRequestDto,
    AnalyseRecalculateResponseDto,
    AnalysesV2Dto,
    AnalyseV2Dto,
    AnalyseV3Dto,
    AsyncAnalyseListResponseDto,
    AsyncAnalyseListResponseV2Dto,
    BulkDeleteAnalyseDto,
    BulkEditAnalyseV2Dto,
    CreateAnalyseAsyncV2Dto,
    CreateAnalyseListAsyncDto,
    EditAnalyseV2Dto,
    PageDtoAnalyseJobDto,
    PageDtoAnalyseReference,
)


class AnalysisOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def delete(self, phrase_token: str, analyseUid: str, purge: bool = None) -> None:
        """
        Delete analysis

        :param phrase_token: string (required) - token to authenticate
        :param analyseUid: string (required), path.
        :param purge: boolean (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def bulkDeleteAnalyses(self, phrase_token: str, body: BulkDeleteAnalyseDto) -> None:
        """
        Delete analyses (batch)

        :param phrase_token: string (required) - token to authenticate
        :param body: BulkDeleteAnalyseDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/analyses/bulk"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def recalculate(
        self, phrase_token: str, body: AnalyseRecalculateRequestDto
    ) -> AnalyseRecalculateResponseDto:
        """
        Recalculate analysis

        :param phrase_token: string (required) - token to authenticate
        :param body: AnalyseRecalculateRequestDto (required), body.

        :return: AnalyseRecalculateResponseDto
        """
        endpoint = f"/api2/v1/analyses/recalculate"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseRecalculateResponseDto(**r)

    def downloadAnalyse(self, phrase_token: str, analyseUid: str, format: str) -> bytes:
        """
        Download analysis

        :param phrase_token: string (required) - token to authenticate
        :param analyseUid: string (required), path.
        :param format: string (required), query.

        :return: None
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/download"
        params = {"format": format}

        files = None
        payload = None

        r = self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    def createAnalysesForProviders(
        self, phrase_token: str, body: CreateAnalyseListAsyncDto
    ) -> AsyncAnalyseListResponseDto:
        """
        Create analyses by providers

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateAnalyseListAsyncDto (required), body.

        :return: AsyncAnalyseListResponseDto
        """
        endpoint = f"/api2/v1/analyses/byProviders"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseDto(**r)

    def createAnalysesForLangs(
        self, phrase_token: str, body: CreateAnalyseListAsyncDto
    ) -> AsyncAnalyseListResponseDto:
        """
        Create analyses by languages

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateAnalyseListAsyncDto (required), body.

        :return: AsyncAnalyseListResponseDto
        """
        endpoint = f"/api2/v1/analyses/byLanguages"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseDto(**r)

    def listJobParts(
        self,
        phrase_token: str,
        analyseLanguagePartId: int,
        analyseUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoAnalyseJobDto:
        """
        List jobs of analyses
        Returns list of job's analyses
        :param phrase_token: string (required) - token to authenticate
        :param analyseLanguagePartId: integer (required), path.
        :param analyseUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoAnalyseJobDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/analyseLanguageParts/{analyseLanguagePartId}/jobs"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseJobDto(**r)

    def getAnalyseLanguagePart(
        self, phrase_token: str, analyseLanguagePartId: int, analyseUid: str
    ) -> AnalyseLanguagePartDto:
        """
        Get analysis language part
        Returns analysis language pair
        :param phrase_token: string (required) - token to authenticate
        :param analyseLanguagePartId: integer (required), path.
        :param analyseUid: string (required), path.

        :return: AnalyseLanguagePartDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/analyseLanguageParts/{analyseLanguagePartId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseLanguagePartDto(**r)

    def getJobPartAnalyse(
        self, phrase_token: str, jobUid: str, analyseUid: str
    ) -> AnalyseJobDto:
        """
        Get jobs analysis
        Returns job's analyse
        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param analyseUid: string (required), path.

        :return: AnalyseJobDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/jobs/{jobUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseJobDto(**r)

    def editAnalysis(
        self, phrase_token: str, analyseUid: str, body: EditAnalyseV2Dto
    ) -> AnalyseV2Dto:
        """
                Edit analysis
                If no netRateScheme is provided in
        request, then netRateScheme associated with provider will be used if it exists, otherwise it will remain the same
        as it was.
                :param phrase_token: string (required) - token to authenticate
                :param analyseUid: string (required), path.
                :param body: EditAnalyseV2Dto (required), body.

                :return: AnalyseV2Dto
        """
        endpoint = f"/api2/v2/analyses/{analyseUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseV2Dto(**r)

    def createAnalyseAsync_1(
        self, phrase_token: str, body: CreateAnalyseAsyncV2Dto
    ) -> AsyncAnalyseListResponseV2Dto:
        """
        Create analysis
        Returns created analyses - batching analyses by number of segments (api.segment.count.approximation, default 100000), in case request contains more segments than maximum (api.segment.max.count, default 300000), returns 400 bad request.
        :param phrase_token: string (required) - token to authenticate
        :param body: CreateAnalyseAsyncV2Dto (required), body.

        :return: AsyncAnalyseListResponseV2Dto
        """
        endpoint = f"/api2/v2/analyses"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseV2Dto(**r)

    def analyses_batchEdit_v2(
        self, phrase_token: str, body: BulkEditAnalyseV2Dto
    ) -> AnalysesV2Dto:
        """
                Edit analyses (batch)
                If no netRateScheme is provided in request, then netRateScheme associated with provider will
        be used if it exists, otherwise it will remain the same as it was.
                :param phrase_token: string (required) - token to authenticate
                :param body: BulkEditAnalyseV2Dto (required), body.

                :return: AnalysesV2Dto
        """
        endpoint = f"/api2/v2/analyses/bulk"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalysesV2Dto(**r)

    def getAnalyseV3(self, phrase_token: str, analyseUid: str) -> AnalyseV3Dto:
        """
        Get analysis

        :param phrase_token: string (required) - token to authenticate
        :param analyseUid: string (required), path.

        :return: AnalyseV3Dto
        """
        endpoint = f"/api2/v3/analyses/{analyseUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseV3Dto(**r)

    def listPartAnalyseV3(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoAnalyseReference:
        """
        List analyses

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :return: PageDtoAnalyseReference
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/analyses"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseReference(**r)
