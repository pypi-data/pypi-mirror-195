from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient


class LanguageQualityAssessmentOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def downloadLqaReports(self, phrase_token: str, jobParts: str) -> bytes:
        """
                Download LQA Assessment XLSX reports
                Returns a single xlsx report or ZIP archive with multiple reports.
        If any given jobPart is not from LQA workflow step, reports from successive workflow steps may be returned
        If none were found returns 404 error, otherwise returns those that were found.
                :param phrase_token: string (required) - token to authenticate
                :param jobParts: string (required), query. Comma separated list of JobPart UIDs.

                :return: None
        """
        endpoint = f"/api2/v1/lqa/assessments/reports"
        params = {"jobParts": jobParts}

        files = None
        payload = None

        r = self.client.get_bytestream(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return r
