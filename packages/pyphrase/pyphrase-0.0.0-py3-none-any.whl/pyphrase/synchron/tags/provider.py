from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ProviderListDtoV2


class ProviderOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listProviders_4(
        self, phrase_token: str, jobUid: str, projectUid: str
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)
