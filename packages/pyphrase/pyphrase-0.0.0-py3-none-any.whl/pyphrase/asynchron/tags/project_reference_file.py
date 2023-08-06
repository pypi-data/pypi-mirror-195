from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateReferenceFileNoteDto,
    ProjectReferenceFilesRequestDto,
    ReferenceFilePageDto,
    ReferenceFileReference,
)


class ProjectReferenceFileOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listReferenceFiles(
        self,
        phrase_token: str,
        projectUid: str,
        createdBy: str = None,
        dateCreatedSince: str = None,
        filename: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "DESC",
    ) -> ReferenceFilePageDto:
        """
        List project reference files

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param createdBy: string (optional), query. UID of user.
        :param dateCreatedSince: string (optional), query. date time in ISO 8601 UTC format.
        :param filename: string (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.

        :return: ReferenceFilePageDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {
            "filename": filename,
            "dateCreatedSince": dateCreatedSince,
            "createdBy": createdBy,
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

        return ReferenceFilePageDto(**r)

    async def createNoteRef(
        self, phrase_token: str, projectUid: str, body: CreateReferenceFileNoteDto
    ) -> ReferenceFileReference:
        """
        Create project reference file
        Accepts `application/octet-stream` or `application/json`.<br>
                       - `application/json` - `note` field will be converted to .txt.<br>
                       - `application/octet-stream` - `Content-Disposition` header is required
        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: CreateReferenceFileNoteDto (required), body.

        :return: ReferenceFileReference
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ReferenceFileReference(**r)

    async def batchDeleteReferenceFiles(
        self, phrase_token: str, projectUid: str, body: ProjectReferenceFilesRequestDto
    ) -> None:
        """
        Delete project reference files (batch)

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def downloadReference(
        self, phrase_token: str, referenceFileId: str, projectUid: str
    ) -> bytes:
        """
        Download project reference file

        :param phrase_token: string (required) - token to authenticate
        :param referenceFileId: string (required), path.
        :param projectUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/{referenceFileId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def batchDownloadReferenceFiles(
        self, phrase_token: str, projectUid: str, body: ProjectReferenceFilesRequestDto
    ) -> bytes:
        """
        Download project reference files (batch)

        :param phrase_token: string (required) - token to authenticate
        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/download"
        params = {}

        files = None
        payload = body

        r = await self.client.post_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r
