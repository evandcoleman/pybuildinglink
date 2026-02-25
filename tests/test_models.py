"""Tests for BuildingLink models."""

from pybuildinglink.models import Package, PackageResponse, EventType


def test_package_response_parsing() -> None:
    """Test parsing a package response."""
    data = {
        "lastRecordVersion": None,
        "entities": [
            {
                "id": "abc-123",
                "counter": 1234,
                "openComment": "TRACK123",
                "openUtc": "2026-02-25T17:06:47Z",
                "eventType": {
                    "id": "type-1",
                    "abbreviatedDescription": "USPS",
                    "eventBackgroundColor": "f88158",
                    "eventFontColor": "000000",
                },
            }
        ],
    }
    response = PackageResponse.model_validate(data)
    assert len(response.entities) == 1
    pkg = response.entities[0]
    assert pkg.carrier == "USPS"
    assert pkg.tracking_number == "TRACK123"


def test_empty_package_response() -> None:
    """Test parsing an empty response."""
    data = {"lastRecordVersion": None, "entities": []}
    response = PackageResponse.model_validate(data)
    assert len(response.entities) == 0
