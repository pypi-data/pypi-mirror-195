from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractConnectorDto,
    AsyncFileOpResponseDto,
    ConnectorCreateResponseDto,
    ConnectorDto,
    ConnectorListDto,
    FileListDto,
    GetFileRequestParamsDto,
    InputStreamLength,
    UploadResultDto,
)


class ConnectorOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getFile(
        self, phrase_token: str, file: str, folder: str, connectorId: str
    ) -> bytes:
        """
        Download file
        Download a file from a subfolder of the selected connector
        :param phrase_token: string (required) - token to authenticate
        :param file: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :return: InputStreamLength
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}/files/{file}"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def getConnector(self, phrase_token: str, connectorId: str) -> ConnectorDto:
        """
        Get a connector

        :param phrase_token: string (required) - token to authenticate
        :param connectorId: string (required), path.

        :return: ConnectorDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConnectorDto(**r)

    async def editConnector(
        self,
        phrase_token: str,
        connectorId: str,
        body: AbstractConnectorDto,
        connectionTest: bool = None,
    ) -> ConnectorCreateResponseDto:
        """
        Edit connector
        Edit selected connector
        :param phrase_token: string (required) - token to authenticate
        :param connectorId: string (required), path.
        :param body: AbstractConnectorDto (required), body.
        :param connectionTest: boolean (optional), query. For running connection test.

        :return: ConnectorCreateResponseDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}"
        params = {"connectionTest": connectionTest}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConnectorCreateResponseDto(**r)

    async def getConnectorList(
        self, phrase_token: str, type: str = None
    ) -> ConnectorListDto:
        """
        List connectors

        :param phrase_token: string (required) - token to authenticate
        :param type: string (optional), query.

        :return: ConnectorListDto
        """
        endpoint = f"/api2/v1/connectors"
        params = {"type": type}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConnectorListDto(**r)

    async def getFolder(
        self,
        phrase_token: str,
        folder: str,
        connectorId: str,
        projectUid: str = None,
        fileType: str = "ALL",
        sort: str = "NAME",
        direction: str = "ASCENDING",
    ) -> FileListDto:
        """
        List files in a subfolder
        List files in a subfolder of the selected connector
        :param phrase_token: string (required) - token to authenticate
        :param folder: string (required), path.
        :param connectorId: string (required), path.
        :param projectUid: string (optional), query.
        :param fileType: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.

        :return: FileListDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}"
        params = {
            "projectUid": projectUid,
            "fileType": fileType,
            "sort": sort,
            "direction": direction,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileListDto(**r)

    async def uploadFile(
        self, phrase_token: str, folder: str, connectorId: str
    ) -> UploadResultDto:
        """
        Upload a file to a subfolder of the selected connector
        Upload a file to a subfolder of the selected connector
        :param phrase_token: string (required) - token to authenticate
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :return: UploadResultDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return UploadResultDto(**r)

    async def getRootFolder(
        self,
        phrase_token: str,
        connectorId: str,
        fileType: str = "ALL",
        sort: str = "NAME",
        direction: str = "ASCENDING",
    ) -> FileListDto:
        """
        List files in root
        List files in a root folder of the selected connector
        :param phrase_token: string (required) - token to authenticate
        :param connectorId: string (required), path.
        :param fileType: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.

        :return: FileListDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders"
        params = {"fileType": fileType, "sort": sort, "direction": direction}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return FileListDto(**r)

    async def getFile_1(
        self,
        phrase_token: str,
        file: str,
        folder: str,
        connectorId: str,
        body: GetFileRequestParamsDto,
    ) -> AsyncFileOpResponseDto:
        """
                Download file (async)
                Create an asynchronous request to download a file from a (sub)folder of the selected connector.
        After a callback with successful response is received, prepared file can be downloaded by [Download prepared file](#operation/getPreparedFile)
        or [Create job from connector asynchronous download task](#operation/createJobFromAsyncDownloadTask).
                :param phrase_token: string (required) - token to authenticate
                :param file: string (required), path.
                :param folder: string (required), path.
                :param connectorId: string (required), path.
                :param body: GetFileRequestParamsDto (required), body.

                :return: AsyncFileOpResponseDto
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{file}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncFileOpResponseDto(**r)

    async def getPreparedFile(
        self, phrase_token: str, taskId: str, file: str, folder: str, connectorId: str
    ) -> bytes:
        """
        Download prepared file
        Download the file by referencing successfully finished async download request [Connector - Download file (async)](#operation/getFile_1).
        :param phrase_token: string (required) - token to authenticate
        :param taskId: string (required), path.
        :param file: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :return: InputStreamLength
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{file}/tasks/{taskId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    async def uploadFile_1(
        self,
        phrase_token: str,
        fileName: str,
        folder: str,
        connectorId: str,
        mimeType: str = None,
    ) -> AsyncFileOpResponseDto:
        """
        Upload file (async)
        Upload a file to a subfolder of the selected connector
        :param phrase_token: string (required) - token to authenticate
        :param fileName: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.
        :param mimeType: string (optional), query. Mime type of the file to upload.

        :return: AsyncFileOpResponseDto
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{fileName}/upload"
        params = {"mimeType": mimeType}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AsyncFileOpResponseDto(**r)
