from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AppleTokenResponseDto,
    LoginDto,
    LoginOtherDto,
    LoginOtherV3Dto,
    LoginResponseDto,
    LoginResponseV3Dto,
    LoginToSessionDto,
    LoginToSessionResponseDto,
    LoginToSessionResponseV3Dto,
    LoginToSessionV3Dto,
    LoginUserDto,
    LoginV3Dto,
    LoginWithAppleDto,
    LoginWithGoogleDto,
)


class AuthenticationOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def login(self, phrase_token: str, body: LoginDto) -> LoginResponseDto:
        """
        Login

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginDto (required), body.

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/login"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def logout(self, phrase_token: str, token: str = None) -> None:
        """
        Logout

        :param phrase_token: string (required) - token to authenticate
        :param token: string (optional), query.

        :return: None
        """
        endpoint = f"/api2/v1/auth/logout"
        params = {"token": token}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def loginToSession(
        self, phrase_token: str, body: LoginToSessionDto
    ) -> LoginToSessionResponseDto:
        """
        Login to session

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginToSessionDto (required), body.

        :return: LoginToSessionResponseDto
        """
        endpoint = f"/api2/v1/auth/loginToSession"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginToSessionResponseDto(**r)

    async def loginOther(
        self, phrase_token: str, body: LoginOtherDto
    ) -> LoginResponseDto:
        """
        Login as another user
        Available only for admin
        :param phrase_token: string (required) - token to authenticate
        :param body: LoginOtherDto (required), body.

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginOther"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def whoAmI(
        self,
        phrase_token: str,
    ) -> LoginUserDto:
        """
        Who am I

        :param phrase_token: string (required) - token to authenticate

        :return: LoginUserDto
        """
        endpoint = f"/api2/v1/auth/whoAmI"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginUserDto(**r)

    async def loginByGoogle(
        self, phrase_token: str, body: LoginWithGoogleDto
    ) -> LoginResponseDto:
        """
        Login with Google

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginWithGoogleDto (required), body.

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithGoogle"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def loginByAppleWithRefreshToken(
        self, phrase_token: str, body: LoginWithAppleDto
    ) -> LoginResponseDto:
        """
        Login with Apple refresh token

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginWithAppleDto (required), body.

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithApple/refreshToken"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def loginByAppleWithCode(
        self, phrase_token: str, body: LoginWithAppleDto, native: bool = None
    ) -> LoginResponseDto:
        """
        Login with Apple with code

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginWithAppleDto (required), body.
        :param native: boolean (optional), query. For sign in with code from native device.

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithApple/code"
        params = {"native": native}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def refreshAppleToken(
        self, phrase_token: str, token: str = None
    ) -> AppleTokenResponseDto:
        """
        refresh apple token

        :param phrase_token: string (required) - token to authenticate
        :param token: string (optional), query.

        :return: AppleTokenResponseDto
        """
        endpoint = f"/api2/v1/auth/refreshAppleToken"
        params = {"token": token}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AppleTokenResponseDto(**r)

    async def login_1(self, phrase_token: str, body: LoginV3Dto) -> LoginResponseV3Dto:
        """
        Login

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginV3Dto (required), body.

        :return: LoginResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/login"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseV3Dto(**r)

    async def loginToSession_2(
        self, phrase_token: str, body: LoginToSessionV3Dto
    ) -> LoginToSessionResponseV3Dto:
        """
        Login to session

        :param phrase_token: string (required) - token to authenticate
        :param body: LoginToSessionV3Dto (required), body.

        :return: LoginToSessionResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/loginToSession"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginToSessionResponseV3Dto(**r)

    async def loginOther_1(
        self, phrase_token: str, body: LoginOtherV3Dto
    ) -> LoginResponseV3Dto:
        """
        Login as another user
        Available only for admin
        :param phrase_token: string (required) - token to authenticate
        :param body: LoginOtherV3Dto (required), body.

        :return: LoginResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/loginOther"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return LoginResponseV3Dto(**r)
