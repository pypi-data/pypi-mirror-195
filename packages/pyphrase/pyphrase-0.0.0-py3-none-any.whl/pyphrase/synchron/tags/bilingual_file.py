from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ComparedSegmentsDto, InputStream, JobPartsDto


class BilingualFileOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def convertBilingualFile(
        self, phrase_token: str, body: InputStream, to: str, frm: str
    ) -> bytes:
        """
        Convert bilingual file

        :param phrase_token: string (required) - token to authenticate
        :param body: InputStream (required), body.
        :param to: string (required), query.
        :param frm: string (required), query.

        :return: None
        """
        endpoint = f"/api2/v1/bilingualFiles/convert"
        params = {"from": frm, "to": to}

        files = None
        payload = body

        r = self.client.post_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r

    def uploadBilingualFile(
        self,
        phrase_token: str,
        body: InputStream,
        format: str = "MXLF",
        saveToTransMemory: str = "Confirmed",
        setCompleted: bool = "False",
    ) -> JobPartsDto:
        """
        Upload bilingual file
        Returns updated job parts
        :param phrase_token: string (required) - token to authenticate
        :param body: InputStream (required), body.
        :param format: string (optional), query.
        :param saveToTransMemory: string (optional), query.
        :param setCompleted: boolean (optional), query.

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/bilingualFiles"
        params = {
            "format": format,
            "saveToTransMemory": saveToTransMemory,
            "setCompleted": setCompleted,
        }

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    def compareBilingualFile(
        self, phrase_token: str, body: InputStream, workflowLevel: int = "1"
    ) -> ComparedSegmentsDto:
        """
        Compare bilingual file
        Compares bilingual file to job state. Returns list of compared segments.
        :param phrase_token: string (required) - token to authenticate
        :param body: InputStream (required), body.
        :param workflowLevel: integer (optional), query.

        :return: ComparedSegmentsDto
        """
        endpoint = f"/api2/v1/bilingualFiles/compare"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ComparedSegmentsDto(**r)

    def getPreviewFile(self, phrase_token: str, body: InputStream) -> bytes:
        """
        Download preview
        Supports mxliff format
        :param phrase_token: string (required) - token to authenticate
        :param body: InputStream (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/bilingualFiles/preview"
        params = {}

        files = None
        payload = body

        r = self.client.post_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r
