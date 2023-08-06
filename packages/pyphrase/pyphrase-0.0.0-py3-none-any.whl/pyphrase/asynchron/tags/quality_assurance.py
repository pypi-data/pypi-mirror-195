from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateLqaProfileDto,
    LqaProfileDetailDto,
    LqaProfileReferenceDto,
    PageDtoLqaProfileReferenceDto,
    QualityAssuranceBatchRunDtoV3,
    QualityAssuranceChecksDtoV2,
    QualityAssuranceResponseDto,
    QualityAssuranceRunDtoV3,
    QualityAssuranceSegmentsRunDtoV3,
    UpdateIgnoredChecksDto,
    UpdateIgnoredWarningsDto,
    UpdateLqaProfileDto,
)


class QualityAssuranceOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def makeDefault(
        self, phrase_token: str, profileUid: str
    ) -> LqaProfileReferenceDto:
        """
        Make LQA profile default

        :param phrase_token: string (required) - token to authenticate
        :param profileUid: string (required), path.

        :return: LqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}/default"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaProfileReferenceDto(**r)

    async def getLqaProfile(
        self, phrase_token: str, profileUid: str
    ) -> LqaProfileDetailDto:
        """
        Get LQA profile details

        :param phrase_token: string (required) - token to authenticate
        :param profileUid: string (required), path.

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    async def updateLqaProfile(
        self, phrase_token: str, profileUid: str, body: UpdateLqaProfileDto
    ) -> LqaProfileDetailDto:
        """
        Update LQA profile

        :param phrase_token: string (required) - token to authenticate
        :param profileUid: string (required), path.
        :param body: UpdateLqaProfileDto (required), body.

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    async def deleteLqaProfile(self, phrase_token: str, profileUid: str) -> None:
        """
        Delete LQA profile

        :param phrase_token: string (required) - token to authenticate
        :param profileUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getLqaProfiles(
        self,
        phrase_token: str,
        order: List[str] = None,
        sort: List[str] = None,
        dateCreated: str = None,
        createdBy: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "20",
    ) -> PageDtoLqaProfileReferenceDto:
        """
        GET list LQA profiles

        :param phrase_token: string (required) - token to authenticate
        :param order: array (optional), query.
        :param sort: array (optional), query.
        :param dateCreated: string (optional), query. It is used for filter the list by date created.
        :param createdBy: string (optional), query. It is used for filter the list by who created the profile.
        :param name: string (optional), query. Name of LQA profiles, it is used for filter the list by name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 20.

        :return: PageDtoLqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles"
        params = {
            "name": name,
            "createdBy": createdBy,
            "dateCreated": dateCreated,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoLqaProfileReferenceDto(**r)

    async def createLqaProfile(
        self, phrase_token: str, body: CreateLqaProfileDto
    ) -> LqaProfileDetailDto:
        """
        Create LQA profile

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateLqaProfileDto (required), body.

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    async def duplicateProfile(
        self, phrase_token: str, profileUid: str
    ) -> LqaProfileReferenceDto:
        """
        Duplicate LQA profile

        :param phrase_token: string (required) - token to authenticate
        :param profileUid: string (required), path.

        :return: LqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}/duplicate"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaProfileReferenceDto(**r)

    async def getLqaProfileAuthors(
        self,
        phrase_token: str,
    ) -> Any:
        """
        Get list of LQA profile authors

        :param phrase_token: string (required) - token to authenticate

        :return:
        """
        endpoint = f"/api2/v1/lqa/profiles/authors"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def updateIgnoredChecks(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredChecksDto,
    ) -> None:
        """
        Edit ignored checks

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredChecksDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoreChecks"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def addIgnoredWarnings(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredWarningsDto,
    ) -> UpdateIgnoredWarningsDto:
        """
        Add ignored warnings

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredWarningsDto (required), body.

        :return: UpdateIgnoredWarningsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoredWarnings"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return UpdateIgnoredWarningsDto(**r)

    async def deleteIgnoredWarnings(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredWarningsDto,
    ) -> None:
        """
        Delete ignored warnings

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredWarningsDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoredWarnings"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def enabledQualityChecksForJob(
        self, phrase_token: str, jobUid: str, projectUid: str
    ) -> QualityAssuranceChecksDtoV2:
        """
        Get QA settings for job
        Returns enabled quality assurance checks and settings for job.
        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :return: QualityAssuranceChecksDtoV2
        """
        endpoint = (
            f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/settings"
        )
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QualityAssuranceChecksDtoV2(**r)

    async def enabledQualityChecksForJob_1(
        self, phrase_token: str, projectUid: str
    ) -> QualityAssuranceChecksDtoV2:
        """
        Get QA settings
        Returns enabled quality assurance checks and settings.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: QualityAssuranceChecksDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/qualityAssurances/settings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QualityAssuranceChecksDtoV2(**r)

    async def runQaForJobPartV3(
        self,
        phrase_token: str,
        jobUid: str,
        projectUid: str,
        body: QualityAssuranceRunDtoV3,
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance
        Call "Get QA settings" endpoint to get the list of enabled QA checks
        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: QualityAssuranceRunDtoV3 (required), body.

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/run"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)

    async def runQaForJobPartsV3(
        self, phrase_token: str, projectUid: str, body: QualityAssuranceBatchRunDtoV3
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance (batch)
        Call "Get QA settings" endpoint to get the list of enabled QA checks
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: QualityAssuranceBatchRunDtoV3 (required), body.

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/qualityAssurances/run"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)

    async def runQaForSegmentsV3(
        self, phrase_token: str, projectUid: str, body: QualityAssuranceSegmentsRunDtoV3
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance on selected segments
        By default runs only fast running checks. Source and target language of jobs have to match.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: QualityAssuranceSegmentsRunDtoV3 (required), body.

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/qualityAssurances/segments/run"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)
