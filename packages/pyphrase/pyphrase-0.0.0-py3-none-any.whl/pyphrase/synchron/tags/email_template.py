from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    OrganizationEmailTemplateDto,
    PageDtoOrganizationEmailTemplateDto,
)


class EmailTemplateOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getOrgEmailTemplate(
        self, phrase_token: str, templateUid: str
    ) -> OrganizationEmailTemplateDto:
        """
        Get email template

        :param phrase_token: string (required) - token to authenticate
        :param templateUid: string (required), path.

        :return: OrganizationEmailTemplateDto
        """
        endpoint = f"/api2/v1/emailTemplates/{templateUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return OrganizationEmailTemplateDto(**r)

    def listOrgEmailTemplates(
        self,
        phrase_token: str,
        type: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoOrganizationEmailTemplateDto:
        """
        List email templates

        :param phrase_token: string (required) - token to authenticate
        :param type: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoOrganizationEmailTemplateDto
        """
        endpoint = f"/api2/v1/emailTemplates"
        params = {"type": type, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoOrganizationEmailTemplateDto(**r)
