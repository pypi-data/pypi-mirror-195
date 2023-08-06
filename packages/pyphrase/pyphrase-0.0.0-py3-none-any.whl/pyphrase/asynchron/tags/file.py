from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    PageDtoUploadedFileDto,
    RemoteUploadedFileDto,
    UploadedFileDto,
)


class FileOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getFileJson(self, phrase_token: str, fileUid: str) -> UploadedFileDto:
        """
        Get file
        Get uploaded file as <b>octet-stream</b> or as <b>json</b> based on 'Accept' header
        :param phrase_token: string (required) - token to authenticate
        :param fileUid: string (required), path.

        :return: UploadedFileDto
        """
        endpoint = f"/api2/v1/files/{fileUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return UploadedFileDto(**r)

    async def deletesFile(self, phrase_token: str, fileUid: str) -> None:
        """
        Delete file

        :param phrase_token: string (required) - token to authenticate
        :param fileUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/files/{fileUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getFiles(
        self,
        phrase_token: str,
        biggerThan: int = None,
        createdBy: int = None,
        types: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoUploadedFileDto:
        """
        List files

        :param phrase_token: string (required) - token to authenticate
        :param biggerThan: integer (optional), query. Size in bytes.
        :param createdBy: integer (optional), query.
        :param types: array (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoUploadedFileDto
        """
        endpoint = f"/api2/v1/files"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "types": types,
            "createdBy": createdBy,
            "biggerThan": biggerThan,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoUploadedFileDto(**r)

    async def createUrlFile(
        self, phrase_token: str, body: RemoteUploadedFileDto
    ) -> UploadedFileDto:
        """
        Upload file
        Accepts multipart/form-data, application/octet-stream or application/json.
        :param phrase_token: string (required) - token to authenticate
        :param body: RemoteUploadedFileDto (required), body. file.

        :return: UploadedFileDto
        """
        endpoint = f"/api2/v1/files"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return UploadedFileDto(**r)
