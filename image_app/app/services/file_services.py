from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import FileExistsError, FileSizeError, FileTypeError
from app.schemas.images import UploadSchema


STATIC_DIR = Path(__file__).parent.parent / "static" / "images"
STATIC_DIR.mkdir(parents=True, exist_ok=True)


class FileHandler:
    @staticmethod
    async def save_file(file: UploadFile, static_dir: Path) -> UploadSchema:
        FileHandler.check_content_type(file)
        FileHandler.check_file_size(file)
        FileHandler.check_file_exists(file, static_dir)

        file_path = f"{static_dir}/{file.filename}"
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        return UploadSchema(
            file_path=file_path, file_name=file.filename, size=file.size
        )  # type: ignore

    @staticmethod
    async def rename_file(file_name: str, new_name: str) -> None:
        Path(file_name).rename(new_name)

    @staticmethod
    def check_content_type(file: UploadFile) -> None:
        if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise FileTypeError()

    @staticmethod
    def check_file_size(file: UploadFile) -> None:
        if file.size is None or file.size > settings.MAX_FILE_SIZE or file.size <= 0:
            raise FileSizeError()

    @staticmethod
    def check_file_exists(file: UploadFile, static_dir: Path) -> None:
        if Path(f"{static_dir}/{file.filename}").exists():
            raise FileExistsError()
