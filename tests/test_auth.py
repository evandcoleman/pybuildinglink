"""Tests for BuildingLink auth."""

from pybuildinglink.auth import BuildingLinkAuth


def test_initial_state() -> None:
    """Test initial auth state."""
    auth = BuildingLinkAuth("test-refresh-token")
    assert auth.refresh_token == "test-refresh-token"
    assert auth.access_token is None
    assert auth.is_token_valid is False
