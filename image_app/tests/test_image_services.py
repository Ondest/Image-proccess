import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.images import ImageSchema
from app.services.image_services import (
    add_new_image,
    get_all_images,
    get_image_by_id,
    delete_image,
    update_image_name,
)


async def test_get_all_images(session_dependency: AsyncSession):
    response = await get_all_images(session=session_dependency)
    assert len(response) == 3


@pytest.mark.parametrize("image_id", [(1), (10000), (-1)])
async def test_get_image_by_id(session_dependency: AsyncSession, image_id: int):
    response = await get_image_by_id(session_dependency, image_id)
    if response:
        schema = ImageSchema.model_validate(response).model_dump()
        del schema["uploaded_at"]
        assert schema == {
            "id": 1,
            "file_name": "image1.jpg",
            "file_path": "/images/image1.jpg",
            "resolution": "1920x1080",
            "size": 204800,
        }
    else:
        assert response is None


@pytest.mark.parametrize("image_id", [(1), (10000)])
async def test_delete_image(session_dependency: AsyncSession, image_id: int):
    response = await delete_image(session=session_dependency, image_id=image_id)
    assert response is None


@pytest.mark.parametrize(
    "image_id, file_name", [(2, "flex.jpeg"), (1000, "false.webp")]
)
async def test_change_image(
    session_dependency: AsyncSession, image_id: int, file_name: str
):
    response = await update_image_name(session_dependency, image_id, file_name)
    if file_name == "flex.jpeg":
        updated_row = await get_image_by_id(session_dependency, image_id)
        assert updated_row.file_name == "flex.jpeg"
    else:
        assert response is None


@pytest.mark.parametrize(
    "file_name, size, resolution, file_path",
    [("moon.jpeg", 10 * 1024, "1920*1080", "/app/app/static/moon.jpeg")],
)
async def test_add_new_image(
    session_dependency: AsyncSession,
    file_name: str,
    size: int,
    resolution: str,
    file_path: str,
):
    await add_new_image(session_dependency, file_name, file_path, size, resolution)
    response = await get_all_images(session_dependency)
    images_name = [
        image.file_name for image in response if image.file_name == file_name
    ]
    assert "moon.jpeg" in images_name
