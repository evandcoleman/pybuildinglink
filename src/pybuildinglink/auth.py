"""OAuth2 authentication for BuildingLink."""

from __future__ import annotations

import time

import aiohttp

from .const import AUTH_URL, CLIENT_ID, USER_AGENT
from .exceptions import AuthenticationError
from .models import TokenResponse


class BuildingLinkAuth:
    """Manage OAuth2 tokens for BuildingLink API."""

    def __init__(self, refresh_token: str) -> None:
        """Initialize with a refresh token."""
        self._refresh_token = refresh_token
        self._access_token: str | None = None
        self._token_expiry: float = 0

    @property
    def refresh_token(self) -> str:
        """Return the current refresh token."""
        return self._refresh_token

    @property
    def access_token(self) -> str | None:
        """Return the current access token."""
        return self._access_token

    @property
    def is_token_valid(self) -> bool:
        """Check if the current access token is still valid."""
        return (
            self._access_token is not None
            and time.time() < self._token_expiry - 30  # 30s buffer
        )

    async def async_refresh_token(
        self, session: aiohttp.ClientSession
    ) -> TokenResponse:
        """Refresh the access token.

        Returns the token response. Updates internal state with new tokens.
        Raises AuthenticationError on failure.
        """
        data = {
            "client_id": CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        }

        try:
            async with session.post(AUTH_URL, data=data, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise AuthenticationError(
                        f"Token refresh failed ({resp.status}): {text}"
                    )
                result = await resp.json()
        except aiohttp.ClientError as err:
            raise AuthenticationError(f"Token refresh request failed: {err}") from err

        token = TokenResponse.model_validate(result)
        self._access_token = token.access_token
        self._refresh_token = token.refresh_token
        self._token_expiry = time.time() + token.expires_in
        return token

    async def async_get_access_token(
        self, session: aiohttp.ClientSession
    ) -> str:
        """Get a valid access token, refreshing if necessary."""
        if not self.is_token_valid:
            await self.async_refresh_token(session)
        assert self._access_token is not None
        return self._access_token
