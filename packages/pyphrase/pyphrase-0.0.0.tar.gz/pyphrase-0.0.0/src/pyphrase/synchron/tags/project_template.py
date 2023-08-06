from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractAnalyseSettingsDto,
    EditAnalyseSettingsDto,
    EditProjectSecuritySettingsDtoV2,
    FileImportSettingsDto,
    MTSettingsPerLanguageListDto,
    PageDtoProjectTemplateReference,
    PageDtoTransMemoryDto,
    PreTranslateSettingsV3Dto,
    ProjectSecuritySettingsDtoV2,
    ProjectTemplateCreateActionDto,
    ProjectTemplateDto,
    ProjectTemplateEditDto,
    ProjectTemplateTermBaseListDto,
    ProjectTemplateTransMemoryListDtoV3,
    ProjectTemplateTransMemoryListV2Dto,
    SetProjectTemplateTermBaseDto,
    SetProjectTemplateTransMemoriesV2Dto,
)


class ProjectTemplateOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def relevantTransMemories(
        self,
        phrase_token: str,
        projectTemplateUid: str,
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
        List project template relevant translation memories

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
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
        endpoint = (
            f"/api2/v1/projectTemplates/{projectTemplateUid}/transMemories/relevant"
        )
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

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    def getProjectTemplates(
        self,
        phrase_token: str,
        businessUnitName: str = None,
        costCenterName: str = None,
        costCenterId: int = None,
        subDomainName: str = None,
        domainName: str = None,
        ownerUid: str = None,
        clientName: str = None,
        clientId: int = None,
        name: str = None,
        sort: str = "dateCreated",
        direction: str = "desc",
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoProjectTemplateReference:
        """
        List project templates

        :param phrase_token: string (required) - token to authenticate
        :param businessUnitName: string (optional), query.
        :param costCenterName: string (optional), query.
        :param costCenterId: integer (optional), query.
        :param subDomainName: string (optional), query.
        :param domainName: string (optional), query.
        :param ownerUid: string (optional), query.
        :param clientName: string (optional), query.
        :param clientId: integer (optional), query.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoProjectTemplateReference
        """
        endpoint = f"/api2/v1/projectTemplates"
        params = {
            "name": name,
            "clientId": clientId,
            "clientName": clientName,
            "ownerUid": ownerUid,
            "domainName": domainName,
            "subDomainName": subDomainName,
            "costCenterId": costCenterId,
            "costCenterName": costCenterName,
            "businessUnitName": businessUnitName,
            "sort": sort,
            "direction": direction,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoProjectTemplateReference(**r)

    def createProjectTemplate(
        self, phrase_token: str, body: ProjectTemplateCreateActionDto
    ) -> ProjectTemplateDto:
        """
        Create project template

        :param phrase_token: string (required) - token to authenticate
        :param body: ProjectTemplateCreateActionDto (required), body.

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def getProjectTemplateTermBases(
        self, phrase_token: str, projectTemplateUid: str
    ) -> ProjectTemplateTermBaseListDto:
        """
        Get term bases

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    def setProjectTemplateTermBases(
        self,
        phrase_token: str,
        projectTemplateUid: str,
        body: SetProjectTemplateTermBaseDto,
    ) -> ProjectTemplateTermBaseListDto:
        """
        Edit term bases in project template

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTermBaseDto (required), body.

        :return: ProjectTemplateTermBaseListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/termBases"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateTermBaseListDto(**r)

    def getProjectTemplateAccessSettings(
        self, phrase_token: str, projectTemplateUid: str
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Get project template access and security settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def editProjectTemplateAccessSettings(
        self,
        phrase_token: str,
        projectTemplateUid: str,
        body: EditProjectSecuritySettingsDtoV2,
    ) -> ProjectSecuritySettingsDtoV2:
        """
        Edit project template access and security settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: EditProjectSecuritySettingsDtoV2 (required), body.

        :return: ProjectSecuritySettingsDtoV2
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/accessSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectSecuritySettingsDtoV2(**r)

    def getProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str
    ) -> ProjectTemplateDto:
        """
        Get project template
        Note: importSettings in response is deprecated and will be always null
        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def editProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str, body: ProjectTemplateEditDto
    ) -> ProjectTemplateDto:
        """
        Edit project template

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: ProjectTemplateEditDto (required), body.

        :return: ProjectTemplateDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateDto(**r)

    def deleteProjectTemplate(self, phrase_token: str, projectTemplateUid: str) -> None:
        """
        Delete project template

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def getAnalyseSettingsForProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str
    ) -> AbstractAnalyseSettingsDto:
        """
        Get analyse settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    def updateAnalyseSettingsForProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str, body: EditAnalyseSettingsDto
    ) -> AbstractAnalyseSettingsDto:
        """
        Edit analyse settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: EditAnalyseSettingsDto (required), body.

        :return: AbstractAnalyseSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AbstractAnalyseSettingsDto(**r)

    def getImportSettingsForProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str
    ) -> FileImportSettingsDto:
        """
        Get import settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    def getMachineTranslateSettingsForProjectTemplate(
        self, phrase_token: str, projectTemplateUid: str
    ) -> MTSettingsPerLanguageListDto:
        """
        Get project template machine translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: MTSettingsPerLanguageListDto
        """
        endpoint = f"/api2/v1/projectTemplates/{projectTemplateUid}/mtSettings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MTSettingsPerLanguageListDto(**r)

    def setProjectTemplateTransMemoriesV2(
        self,
        phrase_token: str,
        projectTemplateUid: str,
        body: SetProjectTemplateTransMemoriesV2Dto,
    ) -> ProjectTemplateTransMemoryListV2Dto:
        """
        Edit translation memories
        If user wants to edit “All target languages” or "All workflow steps”,
                       but there are already varied TM settings for individual languages or steps,
                       then the user risks to overwrite these individual choices.
        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: SetProjectTemplateTransMemoriesV2Dto (required), body.

        :return: ProjectTemplateTransMemoryListV2Dto
        """
        endpoint = f"/api2/v2/projectTemplates/{projectTemplateUid}/transMemories"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListV2Dto(**r)

    def getPreTranslateSettingsForProjectTemplate_2(
        self, phrase_token: str, projectTemplateUid: str
    ) -> PreTranslateSettingsV3Dto:
        """
        Get Pre-translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = (
            f"/api2/v3/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    def updatePreTranslateSettingsForProjectTemplate_2(
        self,
        phrase_token: str,
        projectTemplateUid: str,
        body: PreTranslateSettingsV3Dto,
    ) -> PreTranslateSettingsV3Dto:
        """
        Update Pre-translate settings

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param body: PreTranslateSettingsV3Dto (required), body.

        :return: PreTranslateSettingsV3Dto
        """
        endpoint = (
            f"/api2/v3/projectTemplates/{projectTemplateUid}/preTranslateSettings"
        )
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PreTranslateSettingsV3Dto(**r)

    def getProjectTemplateTransMemories_2(
        self,
        phrase_token: str,
        projectTemplateUid: str,
        wfStepUid: str = None,
        targetLang: str = None,
    ) -> ProjectTemplateTransMemoryListDtoV3:
        """
        Get translation memories

        :param phrase_token: string (required) - token to authenticate
        :param projectTemplateUid: string (required), path.
        :param wfStepUid: string (optional), query. Filter project translation memories by workflow step.
        :param targetLang: string (optional), query. Filter project translation memories by target language.

        :return: ProjectTemplateTransMemoryListDtoV3
        """
        endpoint = f"/api2/v3/projectTemplates/{projectTemplateUid}/transMemories"
        params = {"targetLang": targetLang, "wfStepUid": wfStepUid}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProjectTemplateTransMemoryListDtoV3(**r)
