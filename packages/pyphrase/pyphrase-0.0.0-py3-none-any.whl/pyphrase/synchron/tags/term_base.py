from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    BackgroundTasksTbDto,
    BrowseRequestDto,
    BrowseResponseListDto,
    ConceptDto,
    ConceptEditDto,
    ConceptListReference,
    ConceptListResponseDto,
    ConceptWithMetadataDto,
    CreateTermsDto,
    ImportTermBaseResponseDto,
    InputStream,
    MetadataTbDto,
    PageDtoTermBaseDto,
    SearchInTextResponseList2Dto,
    SearchResponseListTbDto,
    SearchTbByJobRequestDto,
    SearchTbInTextByJobRequestDto,
    SearchTbResponseListDto,
    TermBaseDto,
    TermBaseEditDto,
    TermBaseSearchRequestDto,
    TermCreateDto,
    TermDto,
    TermEditDto,
    TermPairDto,
)


class TermBaseOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def createTermByJob(
        self, phrase_token: str, projectUid: str, jobUid: str, body: CreateTermsDto
    ) -> TermPairDto:
        """
        Create term in job's term bases
        Create new term in the write term base assigned to the job
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: CreateTermsDto (required), body.

        :return: TermPairDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/termBases/createByJob"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermPairDto(**r)

    def getTermBase(self, phrase_token: str, termBaseUid: str) -> TermBaseDto:
        """
        Get term base

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    def updateTermBase(
        self, phrase_token: str, termBaseUid: str, body: TermBaseEditDto
    ) -> TermBaseDto:
        """
        Edit term base
        It is possible to add new languages only
        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: TermBaseEditDto (required), body.

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    def deleteTermBase(
        self, phrase_token: str, termBaseUid: str, purge: bool = "False"
    ) -> None:
        """
        Delete term base

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param purge: boolean (optional), query. purge=false - the Termbase is can later be restored,
                    &#34;purge=true - the Termbase is completely deleted and cannot be restored.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listTermBases(
        self,
        phrase_token: str,
        subDomainId: str = None,
        domainId: str = None,
        clientId: str = None,
        lang: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoTermBaseDto:
        """
        List term bases

        :param phrase_token: string (required) - token to authenticate
        :param subDomainId: string (optional), query.
        :param domainId: string (optional), query.
        :param clientId: string (optional), query.
        :param lang: array (optional), query. Language of the term base.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTermBaseDto
        """
        endpoint = f"/api2/v1/termBases"
        params = {
            "name": name,
            "lang": lang,
            "clientId": clientId,
            "domainId": domainId,
            "subDomainId": subDomainId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTermBaseDto(**r)

    def createTermBase(self, phrase_token: str, body: TermBaseEditDto) -> TermBaseDto:
        """
        Create term base

        :param phrase_token: string (required) - token to authenticate
        :param body: TermBaseEditDto (required), body.

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    def importTermBase(
        self,
        phrase_token: str,
        termBaseUid: str,
        body: InputStream,
        charset: str = "UTF-8",
        strictLangMatching: bool = "False",
        updateTerms: bool = "True",
    ) -> ImportTermBaseResponseDto:
        """
                Upload term base
                Terms can be imported from XLS/XLSX and TBX file formats into a term base.
        See <a target="_blank" href="https://help.memsource.com/hc/en-us/articles/115003681851-Term-Bases">Memsource Wiki</a>
                :param phrase_token: string (required) - token to authenticate
                :param termBaseUid: string (required), path.
                :param body: InputStream (required), body.
                :param charset: string (optional), query.
                :param strictLangMatching: boolean (optional), query.
                :param updateTerms: boolean (optional), query.

                :return: ImportTermBaseResponseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/upload"
        params = {
            "charset": charset,
            "strictLangMatching": strictLangMatching,
            "updateTerms": updateTerms,
        }

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ImportTermBaseResponseDto(**r)

    def listConcepts(
        self,
        phrase_token: str,
        termBaseUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> ConceptListResponseDto:
        """
        List concepts

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: ConceptListResponseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConceptListResponseDto(**r)

    def createConcept(
        self, phrase_token: str, termBaseUid: str, body: ConceptEditDto
    ) -> ConceptWithMetadataDto:
        """
        Create concept

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: ConceptEditDto (required), body.

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    def deleteConcepts(
        self, phrase_token: str, termBaseUid: str, body: ConceptListReference
    ) -> None:
        """
        Delete concepts

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: ConceptListReference (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def getConcept(
        self, phrase_token: str, conceptUid: str, termBaseUid: str
    ) -> ConceptWithMetadataDto:
        """
        Get concept

        :param phrase_token: string (required) - token to authenticate
        :param conceptUid: string (required), path.
        :param termBaseUid: string (required), path.

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    def updateConcept(
        self, phrase_token: str, conceptUid: str, termBaseUid: str, body: ConceptEditDto
    ) -> ConceptWithMetadataDto:
        """
        Update concept

        :param phrase_token: string (required) - token to authenticate
        :param conceptUid: string (required), path.
        :param termBaseUid: string (required), path.
        :param body: ConceptEditDto (required), body.

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    def createTerm(
        self, phrase_token: str, termBaseUid: str, body: TermCreateDto
    ) -> TermDto:
        """
        Create term
        Set conceptId to assign the term to an existing concept, otherwise a new concept will be created.
        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: TermCreateDto (required), body.

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    def clearTermBase(self, phrase_token: str, termBaseUid: str) -> None:
        """
        Clear term base
        Deletes all terms
        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def getTerm(self, phrase_token: str, termId: str, termBaseUid: str) -> TermDto:
        """
        Get term

        :param phrase_token: string (required) - token to authenticate
        :param termId: string (required), path.
        :param termBaseUid: string (required), path.

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    def updateTerm(
        self, phrase_token: str, termId: str, termBaseUid: str, body: TermEditDto
    ) -> TermDto:
        """
        Edit term

        :param phrase_token: string (required) - token to authenticate
        :param termId: string (required), path.
        :param termBaseUid: string (required), path.
        :param body: TermEditDto (required), body.

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    def deleteTerm(self, phrase_token: str, termId: str, termBaseUid: str) -> None:
        """
        Delete term

        :param phrase_token: string (required) - token to authenticate
        :param termId: string (required), path.
        :param termBaseUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def deleteConcept(
        self, phrase_token: str, conceptId: str, termBaseUid: str
    ) -> None:
        """
        Delete concept

        :param phrase_token: string (required) - token to authenticate
        :param conceptId: string (required), path.
        :param termBaseUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listTermsOfConcept(
        self, phrase_token: str, conceptId: str, termBaseUid: str
    ) -> ConceptDto:
        """
        Get terms of concept

        :param phrase_token: string (required) - token to authenticate
        :param conceptId: string (required), path.
        :param termBaseUid: string (required), path.

        :return: ConceptDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptId}/terms"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConceptDto(**r)

    def getLastBackgroundTask(
        self, phrase_token: str, termBaseUid: str
    ) -> BackgroundTasksTbDto:
        """
        Last import status

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.

        :return: BackgroundTasksTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/lastBackgroundTask"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BackgroundTasksTbDto(**r)

    def browseTerms(
        self, phrase_token: str, termBaseUid: str, body: BrowseRequestDto
    ) -> BrowseResponseListDto:
        """
        Browse term base

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: BrowseRequestDto (required), body.

        :return: BrowseResponseListDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/browse"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return BrowseResponseListDto(**r)

    def searchTerms(
        self, phrase_token: str, termBaseUid: str, body: TermBaseSearchRequestDto
    ) -> SearchResponseListTbDto:
        """
        Search term base

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param body: TermBaseSearchRequestDto (required), body.

        :return: SearchResponseListTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/search"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchResponseListTbDto(**r)

    def exportTermBase(
        self,
        phrase_token: str,
        termBaseUid: str,
        termStatus: str = None,
        format: str = "Tbx",
        charset: str = "UTF-8",
    ) -> bytes:
        """
        Export term base

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.
        :param termStatus: string (optional), query.
        :param format: string (optional), query.
        :param charset: string (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/export"
        params = {"format": format, "charset": charset, "termStatus": termStatus}

        files = None
        payload = None

        r = self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    def getTermBaseMetadata(self, phrase_token: str, termBaseUid: str) -> MetadataTbDto:
        """
        Get term base metadata

        :param phrase_token: string (required) - token to authenticate
        :param termBaseUid: string (required), path.

        :return: MetadataTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/metadata"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MetadataTbDto(**r)

    def searchTermsByJob_1(
        self,
        phrase_token: str,
        projectUid: str,
        jobUid: str,
        body: SearchTbByJobRequestDto,
    ) -> SearchTbResponseListDto:
        """
        Search job's term bases
        Search all read term bases assigned to the job
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: SearchTbByJobRequestDto (required), body.

        :return: SearchTbResponseListDto
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/termBases/searchByJob"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchTbResponseListDto(**r)

    def searchTermsInTextByJobV2(
        self,
        phrase_token: str,
        projectUid: str,
        jobUid: str,
        body: SearchTbInTextByJobRequestDto,
    ) -> SearchInTextResponseList2Dto:
        """
        Search terms in text
        Search in text in all read term bases assigned to the job
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: SearchTbInTextByJobRequestDto (required), body.

        :return: SearchInTextResponseList2Dto
        """
        endpoint = (
            f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/termBases/searchInTextByJob"
        )
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchInTextResponseList2Dto(**r)
