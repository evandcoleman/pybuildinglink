"""Tests for BuildingLink auth."""

import pytest
from pybuildinglink.auth import (
    BuildingLinkAuth,
    _get_hidden_inputs,
    _extract_auth_redirect_url,
)
from pybuildinglink.exceptions import AuthenticationError


def test_initial_state_with_credentials() -> None:
    """Test initial auth state with username/password."""
    auth = BuildingLinkAuth(username="user@example.com", password="pass123")
    assert auth.access_token is None
    assert auth.is_token_valid is False
    assert auth.refresh_token is None


def test_initial_state_with_refresh_token() -> None:
    """Test initial auth state with refresh token."""
    auth = BuildingLinkAuth(refresh_token="test-refresh-token")
    assert auth.refresh_token == "test-refresh-token"
    assert auth.access_token is None
    assert auth.is_token_valid is False


def test_requires_some_auth() -> None:
    """Test that at least one auth method is required."""
    with pytest.raises(AuthenticationError):
        BuildingLinkAuth()


def test_get_hidden_inputs() -> None:
    """Test extracting hidden inputs from HTML."""
    html = '''
    <form>
        <input type="hidden" name="csrf" value="abc123" />
        <input type="hidden" name="state" value="xyz" />
        <input type="text" name="username" value="" />
    </form>
    '''
    result = _get_hidden_inputs(html)
    assert result == {"csrf": "abc123", "state": "xyz"}


def test_extract_auth_redirect_url() -> None:
    """Test extracting auth URL from login page content."""
    content = b'var url = "https://auth.buildinglink.com/connect/authorize?foo=bar";'
    url = _extract_auth_redirect_url(content)
    assert url == "https://auth.buildinglink.com/connect/authorize?foo=bar"


def test_extract_auth_redirect_url_not_found() -> None:
    """Test failure when auth URL not in page."""
    with pytest.raises(AuthenticationError):
        _extract_auth_redirect_url(b"no url here")
