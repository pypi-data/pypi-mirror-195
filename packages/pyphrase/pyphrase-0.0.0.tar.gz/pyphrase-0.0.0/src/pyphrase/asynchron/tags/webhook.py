from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateWebHookDto,
    PageDtoWebhookCallDto,
    PageDtoWebHookDtoV2,
    ReplayRequestDto,
    WebHookDtoV2,
    WebhookPreviewsDto,
)


class WebhookOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def replayLast(
        self,
        phrase_token: str,
        status: str = None,
        events: List[str] = None,
        numberOfCalls: int = "5",
    ) -> None:
        """
        Replay last webhook calls
        Replays specified number of last Webhook calls from oldest to the newest one
        :param phrase_token: string (required) - token to authenticate
        :param status: string (optional), query. Status of Webhook calls to filter by.
        :param events: array (optional), query. List of Webhook events to filter by.
        :param numberOfCalls: integer (optional), query. Number of calls to be replayed.

        :return: None
        """
        endpoint = f"/api2/v1/webhooksCalls/replay/latest"
        params = {"numberOfCalls": numberOfCalls, "events": events, "status": status}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getWebhookCallsList(
        self,
        phrase_token: str,
        parentUid: str = None,
        webhookUid: str = None,
        status: str = None,
        events: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
    ) -> PageDtoWebhookCallDto:
        """
        Lists webhook calls

        :param phrase_token: string (required) - token to authenticate
        :param parentUid: string (optional), query. UID of parent webhook call to filter by.
        :param webhookUid: string (optional), query. UID of Webhook to filter by.
        :param status: string (optional), query. Status of Webhook calls to filter by.
        :param events: array (optional), query. List of Webhook events to filter by.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoWebhookCallDto
        """
        endpoint = f"/api2/v1/webhooksCalls"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "events": events,
            "status": status,
            "webhookUid": webhookUid,
            "parentUid": parentUid,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoWebhookCallDto(**r)

    async def replayWebhookCalls(
        self, phrase_token: str, body: ReplayRequestDto
    ) -> None:
        """
        Replay webhook calls
        Replays given list of Webhook Calls in specified order in the request
        :param phrase_token: string (required) - token to authenticate
        :param body: ReplayRequestDto (required), body.

        :return: None
        """
        endpoint = f"/api2/v1/webhooksCalls/replay"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getWebHook_1(self, phrase_token: str, webHookUid: str) -> WebHookDtoV2:
        """
        Get webhook

        :param phrase_token: string (required) - token to authenticate
        :param webHookUid: string (required), path.

        :return: WebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)

    async def updateWebHook_1(
        self, phrase_token: str, webHookUid: str, body: CreateWebHookDto
    ) -> WebHookDtoV2:
        """
        Edit webhook

        :param phrase_token: string (required) - token to authenticate
        :param webHookUid: string (required), path.
        :param body: CreateWebHookDto (required), body.

        :return: WebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)

    async def deleteWebHook_1(self, phrase_token: str, webHookUid: str) -> None:
        """
        Delete webhook

        :param phrase_token: string (required) - token to authenticate
        :param webHookUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v2/webhooks/{webHookUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getWebhookPreviews(
        self, phrase_token: str, events: List[str] = None
    ) -> WebhookPreviewsDto:
        """
        Get webhook body previews

        :param phrase_token: string (required) - token to authenticate
        :param events: array (optional), query. Filter by webhook events, example for multiple: ?events=JOB_CREATED&amp;events=JOB_UPDATED.

        :return: WebhookPreviewsDto
        """
        endpoint = f"/api2/v2/webhooks/previews"
        params = {"events": events}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WebhookPreviewsDto(**r)

    async def sendTestWebhook(
        self, phrase_token: str, webhookUid: str, event: str
    ) -> None:
        """
        Send test webhook

        :param phrase_token: string (required) - token to authenticate
        :param webhookUid: string (required), path. UID of the webhook.
        :param event: string (required), query. Event of test webhook.

        :return: None
        """
        endpoint = f"/api2/v2/webhooks/{webhookUid}/test"
        params = {"event": event}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getWebHookList_1(
        self,
        phrase_token: str,
        sortField: str = None,
        modifiedBy: List[str] = None,
        createdBy: List[str] = None,
        events: List[str] = None,
        url: str = None,
        status: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sortTrend: str = "ASC",
    ) -> PageDtoWebHookDtoV2:
        """
        Lists webhooks

        :param phrase_token: string (required) - token to authenticate
        :param sortField: string (optional), query. Sort by this field.
        :param modifiedBy: array (optional), query. Filter by webhook updaters UIDs.
        :param createdBy: array (optional), query. Filter by webhook creators UIDs.
        :param events: array (optional), query. Filter by webhook events.
        :param url: string (optional), query. Filter by webhook URL.
        :param status: string (optional), query. Filter by enabled/disabled status.
        :param name: string (optional), query. Filter by webhook name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.
        :param sortTrend: string (optional), query. Sort direction.

        :return: PageDtoWebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "status": status,
            "url": url,
            "events": events,
            "createdBy": createdBy,
            "modifiedBy": modifiedBy,
            "sortField": sortField,
            "sortTrend": sortTrend,
        }

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoWebHookDtoV2(**r)

    async def createWebHook_1(
        self, phrase_token: str, body: CreateWebHookDto
    ) -> WebHookDtoV2:
        """
        Create webhook

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateWebHookDto (required), body.

        :return: WebHookDtoV2
        """
        endpoint = f"/api2/v2/webhooks"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WebHookDtoV2(**r)
