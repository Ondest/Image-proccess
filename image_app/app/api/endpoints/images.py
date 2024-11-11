from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile, status
from fastapi_cache.decorator import cache
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_auth_user
from app.db.database import db_handler
from app.schemas.images import ImageSchema, UploadSchema
from app.services.image_services import get_all_images, get_image_by_id
from app.services.use_cases.change_file_name_use_case import ChangeFileNameUseCase
from app.services.use_cases.file_delete_use_case import FileDeleteUseCase
from app.services.use_cases.file_upload_use_case import FileUploadUseCase


router = APIRouter()


@router.get("")
@cache(expire=30)
async def get_images(
    session: AsyncSession = Depends(db_handler.session_dependency),
) -> Sequence[ImageSchema]:
    images = await get_all_images(session=session)
    return images


@router.get("/{image_id}")
@cache(expire=10)
async def get_image(
    image_id: Annotated[
        int, Path(..., gt=0, description="Image id must be greater then 0")
    ],
    session: AsyncSession = Depends(db_handler.session_dependency),
) -> ImageSchema | None:
    image = await get_image_by_id(session=session, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post("/upload_image", status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_handler.session_dependency),
    user: dict[str, str] = Depends(get_current_auth_user),
) -> UploadSchema:
    use_case = FileUploadUseCase(file, session)
    file_data = await use_case.execute()
    return file_data


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    id: Annotated[int, Field(..., gt=0, description="Image id must be greater then 0")],
    session: AsyncSession = Depends(db_handler.session_dependency),
    user: dict[str, str] = Depends(get_current_auth_user),
) -> None:
    use_case = FileDeleteUseCase(session, id)
    await use_case.execute()


@router.patch("/{image_id}")
async def change_image(
    id: Annotated[int, Field(..., gt=0, description="Image id must be greater then 0")],
    name: Annotated[
        str,
        Field(
            ..., max_length=30, description="Image name length should be less then 30"
        ),
    ],
    session: AsyncSession = Depends(db_handler.session_dependency),
    user: dict[str, str] = Depends(get_current_auth_user),
) -> None:
    use_case = ChangeFileNameUseCase(id, name, session)
    await use_case.execute()
