from typing import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Image
from app.schemas.images import ImageSchema


async def get_all_images(session: AsyncSession) -> Sequence[ImageSchema]:
    stmt = select(Image).order_by(Image.uploaded_at)
    result = await session.scalars(stmt)
    return [ImageSchema.model_validate(image) for image in result.all() if image]


async def get_image_by_id(session: AsyncSession, image_id: int):
    stmt = select(Image).filter_by(id=image_id)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def add_new_image(
    session: AsyncSession, file_name: str, file_path: str, size: int, resolution: str
) -> None:
    stmt = insert(Image).values(
        file_path=file_path, size=size, resolution=resolution, file_name=file_name
    )
    await session.execute(stmt)
    await session.commit()


async def delete_image(session: AsyncSession, image_id: int) -> None:
    stmt = delete(Image).where(Image.id == image_id)
    await session.execute(stmt)
    await session.commit()


async def update_image_name(session: AsyncSession, image_id: int, name: str) -> None:
    stmt = update(Image).where(Image.id == image_id).values(file_name=name)
    await session.execute(stmt)
    await session.commit()
