# pybuildinglink

Async Python client for the [BuildingLink](https://www.buildinglink.com/) resident API.

Built for use with [Home Assistant](https://www.home-assistant.io/) but works standalone.

## Installation

```bash
pip install pybuildinglink
```

## Usage

```python
import asyncio
from pybuildinglink import BuildingLinkClient

async def main():
    async with BuildingLinkClient(refresh_token="your-refresh-token") as client:
        # Get open packages
        packages = await client.async_get_packages()
        for pkg in packages:
            print(f"{pkg.carrier}: {pkg.tracking_number}")

        # Get maintenance requests
        requests = await client.async_get_maintenance_requests()
        print(f"{len(requests)} open maintenance requests")

        # Get announcements
        announcements = await client.async_get_announcements()
        for ann in announcements:
            print(f"{ann.title}: {ann.body}")

        # Get calendar events
        events = await client.async_get_calendar_events(
            from_date="2026-01-01T00:00:00",
            to_date="2026-12-31T23:59:59",
        )

        # Get amenity reservations
        reservations = await client.async_get_amenity_reservations()

        # Get user profile
        profile = await client.async_get_user_profile()
        print(f"Logged in as {profile.first_name} {profile.last_name}")

asyncio.run(main())
```

## Authentication

BuildingLink uses OAuth2 with refresh tokens. You need a valid refresh token from the BuildingLink iOS app. The client automatically refreshes the access token (15 min expiry) as needed.

The refresh token is rotated on each use — the client tracks the latest one via `client.refresh_token`.

## API Coverage

| Endpoint | Method |
|---|---|
| Packages/Deliveries | `async_get_packages()` |
| Maintenance Requests | `async_get_maintenance_requests()` |
| Announcements | `async_get_announcements()` |
| Calendar Events | `async_get_calendar_events()` |
| Amenities | `async_get_amenities()` |
| Amenity Reservations | `async_get_amenity_reservations()` |
| Building Contacts | `async_get_contacts()` |
| User Profile | `async_get_user_profile()` |
| Front Desk Instructions | `async_get_front_desk_instructions()` |
| Authorized Properties | `async_get_properties()` |

## License

MIT
