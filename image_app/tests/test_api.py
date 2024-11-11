import pytest
from httpx import AsyncClient


async def test_true_is_true():
    assert True is True, "Skipping startup event loop error"


@pytest.mark.parametrize(
    "expected_status, url, amount",
    [
        (200, "/images", 3),
        (404, "/image", 1),
    ],
)
async def test_get_images(
    a_client: AsyncClient, expected_status: int, url: str, amount: int
):
    response = await a_client.get(url)
    assert response.status_code == expected_status
    assert len(response.json()) == amount


@pytest.mark.parametrize(
    "expected_status, data, id",
    [
        (
            200,
            {
                "id": 1,
                "file_name": "image1.jpg",
                "file_path": "/images/image1.jpg",
                "resolution": "1920x1080",
                "size": 204800,
            },
            1,
        ),
        (404, {"detail": "Image not found"}, 1000),
    ],
)
async def test_get_image(
    a_client: AsyncClient, expected_status: int, data: dict[str, int | str], id: int
):
    response = await a_client.get(f"/images/{id}")
    assert response.status_code == expected_status
    result = response.json()
    result.pop("uploaded_at", None)
    assert result == data


@pytest.mark.parametrize(
    "user, expected_status",
    [
        (
            {"username": "bill", "password": "earth", "email": "some@mail.com"},
            201,
        ),
        (
            {"username": "bill", "password": "earth", "email": "some@mail.com"},
            400,
        ),
        (
            {"username": "sam", "password": "moon", "email": "somemail.com"},
            422,
        ),
    ],
)
async def test_add_user(
    a_client: AsyncClient,
    user: dict[str, str],
    expected_status: int,
):
    result = await a_client.post(url="/auth/users/add/", data=user)
    assert result.status_code == expected_status, "Wrong server status code"
