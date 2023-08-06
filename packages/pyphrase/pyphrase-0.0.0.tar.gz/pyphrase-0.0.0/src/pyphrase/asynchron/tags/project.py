from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractProjectDto,
    AbstractProjectDtoV2,
    AddTargetLangDto,
    AddWorkflowStepsDto,
    AnalyseSettingsDto,
    AssignableTemplatesDto,
    AssignVendorDto,
    AsyncRequestWrapperV2Dto,
    CloneProjectDto,
    CreateProjectFromTemplateAsyncV2Dto,
    CreateProjectFromTemplateV2Dto,
    CreateProjectV3Dto,
    EditProjectMTSettingsDto,
    EditProjectMTSettPerLangListDto,
    EditProjectSecuritySettingsDtoV2,
    EditProjectV2Dto,
    EditQASettingsDtoV2,
    EnabledQualityChecksDto,
    FileImportSettingsCreateDto,
    FileImportSettingsDto,
    FileNamingSettingsDto,
    FinancialSettingsDto,
    JobPartReferences,
    JobPartsDto,
    LqaSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoAbstractProjectDto,
    PageDtoAnalyseReference,
    PageDtoProviderReference,
    PageDtoQuoteDto,
    PageDtoTermBaseDto,
    PageDtoTransMemoryDto,
    PatchProjectDto,
    PreTranslateSettingsV3Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTermBaseListDto,
    ProjectTransMemoryListDtoV3,
    ProjectWorkflowStepListDtoV2,
    ProviderListDtoV2,
    QASettingsDtoV2,
    SearchResponseListTmDto,
    SearchTMRequestDto,
    SetFinancialSettingsDto,
    SetProjectStatusDto,
    SetProjectTransMemoriesV3Dto,
    SetTermBaseDto,
)


class ProjectOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def assignLinguistsFromTemplateToJobParts(
        self,
        phrase_token: str,
        projectUid: str,
        templateUid: str,
        body: JobPartReferences,
    ) -> JobPartsDto:
        """
        Assigns providers from template (specific jobs)

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param templateUid: string (required), path.
        :param body: JobPartReferences (required), body.

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders/forJobParts"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def listProjects(
        self,
        phrase_token: str,
        nameOrInternalId: str = None,
        buyerId: int = None,
        jobStatusGroup: str = None,
        jobStatuses: List[str] = None,
        ownerId: int = None,
        sourceLangs: List[str] = None,
        createdInLastHours: int = None,
        dueInHours: int = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        subDomainId: int = None,
        domainName: str = None,
        domainId: int = None,
        targetLangs: List[str] = None,
        statuses: List[str] = None,
        businessUnitName: str = None,
        businessUnitId: int = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        includeArchived: bool = "False",
        archivedOnly: bool = "False",
    ) -> PageDtoAbstractProjectDto:
        """
        List projects

        :param phrase_token: string (required) - token to authenticate
        :param nameOrInternalId: string (optional), query. Name or internal ID of project.
        :param buyerId: integer (optional), query.
        :param jobStatusGroup: string (optional), query. Allowed for linguists only.
        :param jobStatuses: array (optional), query. Allowed for linguists only.
        :param ownerId: integer (optional), query.
        :param sourceLangs: array (optional), query.
        :param createdInLastHours: integer (optional), query.
        :param dueInHours: integer (optional), query. -1 for projects that are overdue.
        :param costCenterName: string (optional), query.
        :param costCenterId: integer (optional), query.
        :param subDomainName: string (optional), query.
        :param subDomainId: integer (optional), query.
        :param domainName: string (optional), query.
        :param domainId: integer (optional), query.
        :param targetLangs: array (optional), query.
        :param statuses: array (optional), query.
        :param businessUnitName: string (optional), query.
        :param businessUnitId: integer (optional), query.
        :param clientName: string (optional), query.
        :param clientId: integer (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param includeArchived: boolean (optional), query. List also archived projects.
        :param archivedOnly: boolean (optional), query. List only archived projects, regardless of `includeArchived`.

        :return: PageDtoAbstractProjectDto
        """
        endpoint = f"/api2/v1/projects"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "businessUnitId": businessUnitId,
            "businessUnitName": businessUnitName,
            "statuses": statuses,
            "targetLangs": targetLangs,
            "domainId": domainId,
            "domainName": domainName,
            "subDomainId": subDomainId,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "dueInHours": dueInHours,
            "createdInLastHours": createdInLastHours,
            "sourceLangs": sourceLangs,
            "ownerId": ownerId,
            "jobStatuses": jobStatuses,
            "jobStatusGroup": jobStatusGroup,
            "buyerId": buyerId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "nameOrInternalId": nameOrInternalId,
            "includeArchived": includeArchived,
            "archivedOnly": archivedOnly,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAbstractProjectDto(**r)

    async def getProject(
        self, phrase_token: str, projectUid: str
    ) -> AbstractProjectDto:
        """
        Get project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def deleteProject(
        self, phrase_token: str, projectUid: str, purge: bool = "False"
    ) -> None:
        """
        Delete project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param purge: boolean (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def patchProject(
        self, phrase_token: str, projectUid: str, body: PatchProjectDto
    ) -> AbstractProjectDto:
        """
        Edit project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: PatchProjectDto (required), body.

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def addTargetLanguageToProject(
        self, phrase_token: str, projectUid: str, body: AddTargetLangDto
    ) -> None:
        """
        Add target languages
        Add target languages to project
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: AddTargetLangDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/targetLangs"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def addWorkflowSteps(
        self, phrase_token: str, projectUid: str, body: AddWorkflowStepsDto
    ) -> None:
        """
        Add workflow steps

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: AddWorkflowStepsDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/workflowSteps"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def assignVendorToProject(
        self, phrase_token: str, projectUid: str, body: AssignVendorDto
    ) -> None:
        """
                Assign vendor
                To unassign Vendor from Project, use empty body:
        ```
        {}
        ```
                :param phrase_token: string (required) - token to authenticate
                :param projectUid: string (required), path.
                :param body: AssignVendorDto (required), body.

                :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignVendor"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def cloneProject(
        self, phrase_token: str, projectUid: str, body: CloneProjectDto
    ) -> AbstractProjectDto:
        """
        Clone project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: CloneProjectDto (required), body.

        :return: AbstractProjectDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/clone"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDto(**r)

    async def getProjectAssignments(
        self,
        phrase_token: str,
        projectUid: str,
        providerName: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoProviderReference:
        """
        List project providers

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param providerName: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoProviderReference
        """
        endpoint = f"/api2/v1/projects/{projectUid}/providers"
        params = {
            "providerName": providerName,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoProviderReference(**r)

    async def setProjectStatus(
        self, phrase_token: str, projectUid: str, body: SetProjectStatusDto
    ) -> None:
        """
        Edit project status

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: SetProjectStatusDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/setStatus"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def assignableTemplates(
        self, phrase_token: str, projectUid: str
    ) -> AssignableTemplatesDto:
        """
        List assignable templates

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: AssignableTemplatesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/assignableTemplates"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AssignableTemplatesDto(**r)

    async def assignLinguistsFromTemplate(
        self, phrase_token: str, projectUid: str, templateUid: str
    ) -> JobPartsDto:
        """
        Assigns providers from template

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param templateUid: string (required), path.

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/applyTemplate/{templateUid}/assignProviders"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def getFinancialSettings(
        self, phrase_token: str, projectUid: str
    ) -> FinancialSettingsDto:
        """
        Get financial settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    async def setFinancialSettings(
        self, phrase_token: str, projectUid: str, body: SetFinancialSettingsDto
    ) -> FinancialSettingsDto:
        """
        Edit financial settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: SetFinancialSettingsDto (required), body.

        :return: FinancialSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/financialSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FinancialSettingsDto(**r)

    async def enabledQualityChecks(
        self, phrase_token: str, projectUid: str
    ) -> EnabledQualityChecksDto:
        """
        Get QA checks
        Returns enabled quality assurance settings.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: EnabledQualityChecksDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/qaSettingsChecks"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return EnabledQualityChecksDto(**r)

    async def getProjectSettings(
        self, phrase_token: str, projectUid: str, workflowLevel: int = "1"
    ) -> LqaSettingsDto:
        """
        Get LQA settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param workflowLevel: integer (optional), query.

        :return: LqaSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/lqaSettings"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LqaSettingsDto(**r)

    async def getMtSettingsForProject(
        self, phrase_token: str, projectUid: str
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project machine translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def setMtSettingsForProject(
        self, phrase_token: str, projectUid: str, body: EditProjectMTSettingsDto
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings
        This will erase all mtSettings per language for project.
        To remove all machine translate settings from project call without a machineTranslateSettings parameter.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettingsDto (required), body.

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def getQuotesForProject(
        self,
        phrase_token: str,
        projectUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoQuoteDto:
        """
        List quotes

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoQuoteDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/quotes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoQuoteDto(**r)

    async def setMtSettingsPerLanguageForProject(
        self, phrase_token: str, projectUid: str, body: EditProjectMTSettPerLangListDto
    ) -> MTSettingsPerLanguageListDto:
        """
        Edit machine translate settings per language
        This will erase mtSettings for project
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: EditProjectMTSettPerLangListDto (required), body.

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/mtSettingsPerLanguage"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    async def getAnalyseSettingsForProject(
        self, phrase_token: str, projectUid: str
    ) -> AnalyseSettingsDto:
        """
        Get analyse settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: AnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AnalyseSettingsDto(**r)

    async def getImportSettings_2(
        self, phrase_token: str, projectUid: str
    ) -> FileImportSettingsDto:
        """
        Get projects's default import settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def editImportSettings_1(
        self, phrase_token: str, projectUid: str, body: FileImportSettingsCreateDto
    ) -> FileImportSettingsDto:
        """
        Edit project import settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: FileImportSettingsCreateDto (required), body.

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def getFileNamingSettings(
        self, phrase_token: str, projectUid: str
    ) -> FileNamingSettingsDto:
        """
        Get file naming settings for project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    async def updateFileNamingSettings(
        self, phrase_token: str, projectUid: str, body: FileNamingSettingsDto
    ) -> FileNamingSettingsDto:
        """
        Update file naming settings for project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: FileNamingSettingsDto (required), body.

        :return: FileNamingSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileNamingSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileNamingSettingsDto(**r)

    async def getProjectTermBases(
        self, phrase_token: str, projectUid: str
    ) -> ProjectTermBaseListDto:
        """
        Get term bases

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    async def setProjectTermBases(
        self, phrase_token: str, projectUid: str, body: SetTermBaseDto
    ) -> ProjectTermBaseListDto:
        """
        Edit term bases

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: SetTermBaseDto (required), body.

        :return: ProjectTermBaseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTermBaseListDto(**r)

    async def relevantTermBases(
        self,
        phrase_token: str,
        projectUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoTermBaseDto:
        """
        List project relevant term bases

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTermBaseDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/termBases/relevant"
        params = {
            "name": name,
            "domainName": domainName,
            "clientName": clientName,
            "subDomainName": subDomainName,
            "targetLangs": targetLangs,
            "strictLangMatching": strictLangMatching,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTermBaseDto(**r)

    async def relevantTransMemories_1(
        self,
        phrase_token: str,
        projectUid: str,
        targetLangs: List[str] = None,
        subDomainName: str = None,
        clientName: str = None,
        domainName: str = None,
        name: str = None,
        strictLangMatching: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoTransMemoryDto:
        """
        List project relevant translation memories

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param targetLangs: array (optional), query.
        :param subDomainName: string (optional), query.
        :param clientName: string (optional), query.
        :param domainName: string (optional), query.
        :param name: string (optional), query.
        :param strictLangMatching: boolean (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoTransMemoryDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/transMemories/relevant"
        params = {
            "name": name,
            "domainName": domainName,
            "clientName": clientName,
            "subDomainName": subDomainName,
            "targetLangs": targetLangs,
            "strictLangMatching": strictLangMatching,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    async def searchSegment_1(
        self, phrase_token: str, projectUid: str, body: SearchTMRequestDto
    ) -> SearchResponseListTmDto:
        """
        Search translation memory for segment in the project
        Returns at most <i>maxSegments</i>
            records with <i>score >= scoreThreshold</i> and at most <i>maxSubsegments</i> records which are subsegment,
            i.e. the source text is substring of the query text.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: SearchTMRequestDto (required), body.

        :return: SearchResponseListTmDto
        """
        endpoint = (
            f"/api2/v1/projects/{projectUid}/transMemories/searchSegmentInProject"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    async def setProjectQASettingsV2(
        self, phrase_token: str, projectUid: str, body: EditQASettingsDtoV2
    ) -> QASettingsDtoV2:
        """
        Edit quality assurance settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: EditQASettingsDtoV2 (required), body.

        :return: QASettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/qaSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return QASettingsDtoV2(**r)

    async def createProjectFromTemplateV2(
        self, phrase_token: str, templateUid: str, body: CreateProjectFromTemplateV2Dto
    ) -> AbstractProjectDtoV2:
        """
        Create project from template

        :param phrase_token: string (required) - token to authenticate
        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateV2Dto (required), body.

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/applyTemplate/{templateUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def createProjectFromTemplateV2Async(
        self,
        phrase_token: str,
        templateUid: str,
        body: CreateProjectFromTemplateAsyncV2Dto,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Create project from template (async)

        :param phrase_token: string (required) - token to authenticate
        :param templateUid: string (required), path.
        :param body: CreateProjectFromTemplateAsyncV2Dto (required), body.

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/projects/applyTemplate/async/{templateUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)

    async def getProjectAccessSettingsV2(
        self, phrase_token: str, projectUid: str
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get access and security settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def editProjectAccessSettingsV2(
        self, phrase_token: str, projectUid: str, body: EditProjectSecuritySettingsDtoV2
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit access and security settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    async def getProjectWorkflowStepsV2(
        self, phrase_token: str, projectUid: str, withAssignedJobs: bool = "False"
    ) -> ProjectWorkflowStepListDtoV2:
        """
        Get workflow steps

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param withAssignedJobs: boolean (optional), query. Return only steps containing jobs assigned to the calling linguist..

        :return: ProjectWorkflowStepListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/workflowSteps"
        params = {"withAssignedJobs": withAssignedJobs}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectWorkflowStepListDtoV2(**r)

    async def editProjectV2(
        self, phrase_token: str, projectUid: str, body: EditProjectV2Dto
    ) -> AbstractProjectDtoV2:
        """
        Edit project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: EditProjectV2Dto (required), body.

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def listProviders_3(
        self, phrase_token: str, projectUid: str
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)

    async def getPreTranslateSettingsForProject_2(
        self, phrase_token: str, projectUid: str
    ) -> PreTranslateSettingsV3Dto:
        """
        Get Pre-translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    async def editProjectPreTranslateSettings_2(
        self, phrase_token: str, projectUid: str, body: PreTranslateSettingsV3Dto
    ) -> PreTranslateSettingsV3Dto:
        """
        Update Pre-translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: PreTranslateSettingsV3Dto (required), body.

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/preTranslateSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    async def createProjectV3(
        self, phrase_token: str, body: CreateProjectV3Dto
    ) -> AbstractProjectDtoV2:
        """
        Create project

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateProjectV3Dto (required), body.

        :return: AbstractProjectDtoV2
        """
        endpoint = f"/api2/v3/projects"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractProjectDtoV2(**r)

    async def listByProjectV3(
        self,
        phrase_token: str,
        projectUid: str,
        onlyOwnerOrg: bool = None,
        uid: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "desc",
    ) -> PageDtoAnalyseReference:
        """
        List analyses by project

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param onlyOwnerOrg: boolean (optional), query.
        :param uid: string (optional), query. Uid to search by.
        :param name: string (optional), query. Name to search by.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sort: string (optional), query. Sorting field.
        :param order: string (optional), query. Sorting order.

        :return: PageDtoAnalyseReference
        """
        endpoint = f"/api2/v3/projects/{projectUid}/analyses"
        params = {
            "name": name,
            "uid": uid,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
            "onlyOwnerOrg": onlyOwnerOrg,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseReference(**r)

    async def getProjectTransMemories_1(
        self,
        phrase_token: str,
        projectUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
    ) -> ProjectTransMemoryListDtoV3:
        """
        Get translation memories

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)

    async def setProjectTransMemoriesV3(
        self, phrase_token: str, projectUid: str, body: SetProjectTransMemoriesV3Dto
    ) -> ProjectTransMemoryListDtoV3:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: SetProjectTransMemoriesV3Dto (required), body.

        :return: ProjectTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTransMemoryListDtoV3(**r)
