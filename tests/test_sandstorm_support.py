from datasette.app import Datasette
import pytest


@pytest.fixture
def ds():
    return Datasette(memory=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "headers,expected",
    (
        ({}, None),
        (
            {"X-Sandstorm-User-Id": "1", "X-Sandstorm-Username": "abc"},
            {"id": "1", "username": "abc"},
        ),
        (
            {
                "X-Sandstorm-Permissions": "permissions",
                "X-Sandstorm-Preferred-Handle": "preferred_handle",
                "X-Sandstorm-User-Picture": "picture",
                "X-Sandstorm-User-Pronouns": "pronouns",
            },
            {
                "permissions": "permissions",
                "preferred_handle": "preferred_handle",
                "picture": "picture",
                "pronouns": "pronouns",
            },
        ),
    ),
)
async def test_actor_from_headers(ds, headers, expected):
    response = await ds.client.get("/-/actor.json", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"actor": expected}
