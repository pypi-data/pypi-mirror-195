from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    ConversationListDto,
    EditPlainConversationDto,
    FindConversationsDto,
    LQAConversationDto,
    LQAConversationsListDto,
    PlainConversationDto,
    PlainConversationsListDto,
)


class ConversationsOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listAllConversations(
        self,
        phrase_token: str,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
    ) -> ConversationListDto:
        """
        List all conversations

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :return: ConversationListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    def findConversations(
        self, phrase_token: str, body: FindConversationsDto
    ) -> ConversationListDto:
        """
        Find all conversation

        :param phrase_token: string (required) - token to authenticate
        :param body: FindConversationsDto (required), body.

        :return: ConversationListDto
        """
        endpoint = f"/api2/v1/jobs/conversations/find"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    def deleteLQAComment(
        self, phrase_token: str, commentId: str, conversationId: str, jobUid: str
    ) -> None:
        """
        Delete LQA comment

        :param phrase_token: string (required) - token to authenticate
        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def getLQAConversation(
        self, phrase_token: str, conversationId: str, jobUid: str
    ) -> LQAConversationDto:
        """
        Get LQA conversation

        :param phrase_token: string (required) - token to authenticate
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    def deleteLQAConversation(
        self, phrase_token: str, conversationId: str, jobUid: str
    ) -> None:
        """
        Delete LQA conversation

        :param phrase_token: string (required) - token to authenticate
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listLQAConversations(
        self,
        phrase_token: str,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
    ) -> LQAConversationsListDto:
        """
        List LQA conversations

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :return: LQAConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LQAConversationsListDto(**r)

    def getPlainConversation(
        self, phrase_token: str, conversationId: str, jobUid: str
    ) -> PlainConversationDto:
        """
        Get plain conversation

        :param phrase_token: string (required) - token to authenticate
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    def updatePlainConversation(
        self,
        phrase_token: str,
        conversationId: str,
        jobUid: str,
        body: EditPlainConversationDto,
    ) -> PlainConversationDto:
        """
        Edit plain conversation

        :param phrase_token: string (required) - token to authenticate
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: EditPlainConversationDto (required), body.

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    def deletePlainConversation(
        self, phrase_token: str, conversationId: str, jobUid: str
    ) -> None:
        """
        Delete plain conversation

        :param phrase_token: string (required) - token to authenticate
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    def listPlainConversations(
        self,
        phrase_token: str,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
    ) -> PlainConversationsListDto:
        """
        List plain conversations

        :param phrase_token: string (required) - token to authenticate
        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :return: PlainConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PlainConversationsListDto(**r)

    def deletePlainComment(
        self, phrase_token: str, commentId: str, conversationId: str, jobUid: str
    ) -> None:
        """
        Delete plain comment

        :param phrase_token: string (required) - token to authenticate
        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return
