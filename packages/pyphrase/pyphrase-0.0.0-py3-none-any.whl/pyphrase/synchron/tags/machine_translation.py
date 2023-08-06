from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    MachineTranslateResponse,
    TranslationRequestExtendedDto,
)


class MachineTranslationOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def machineTranslation(
        self, phrase_token: str, mtSettingsUid: str, body: TranslationRequestExtendedDto
    ) -> MachineTranslateResponse:
        """
        Translate with MT

        :param phrase_token: string (required) - token to authenticate
        :param mtSettingsUid: string (required), path.
        :param body: TranslationRequestExtendedDto (required), body.

        :return: MachineTranslateResponse
        """
        endpoint = f"/api2/v1/machineTranslations/{mtSettingsUid}/translate"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return MachineTranslateResponse(**r)
