import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_dummy_model(
    client: AsyncClient,
) -> None:
    """Tests dummy instance creation."""
    test_name = "test_name"
    response = await client.post(
        "/api/dummy/",
        json={
            "name": test_name,
        },
    )
    assert response.status_code == 201
