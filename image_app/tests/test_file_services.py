from fastapi import UploadFile
import pytest
from starlette.datastructures import Headers
from app.services.file_services import FileHandler
from app.core.exceptions import FileTypeError, FileSizeError, FileExistsError
from pathlib import Path
import os


ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/gif"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mb


@pytest.mark.parametrize(
    "file_content_type, file_size, should_succeed, expected_exception, file_name",
    [
        ("image/jpeg", 512 * 1024, True, None, "test.jpeg"),
        ("application/pdf", 512 * 1024, False, FileTypeError, "1.jpeg"),
        ("image/png", 12 * 1024 * 1024, False, FileSizeError, "2.jpeg"),
        ("image/jpeg", 0, False, FileSizeError, "3.jpeg"),
        ("image/jpeg", 512 * 1024, False, FileExistsError, "test.jpeg"),
    ],
)
async def test_save_file(
    file_content_type: str,
    file_size: int,
    should_succeed: bool,
    expected_exception: Exception,
    file_upload: UploadFile,
    temp_dir_for_tests: Path,
    file_name: str,
):
    file_upload.filename = file_name
    file_upload.headers = Headers({"content-type": file_content_type})
    file_upload.size = file_size
    STATIC_DIR = temp_dir_for_tests

    if should_succeed:
        await FileHandler.save_file(file_upload, STATIC_DIR)
        assert Path(f"{STATIC_DIR}/{file_upload.filename}").exists()

    else:
        with pytest.raises(expected_exception):
            await FileHandler.save_file(file_upload, STATIC_DIR)


async def test_rename_file(temp_dir_for_tests):
    static_dir = temp_dir_for_tests
    old_file = os.path.join(static_dir, "image1.jpeg")
    with open(old_file, "w") as f:
        f.write("This is a test file.")

    new_file = old_file.replace("image1.jpeg", "1image.jpeg")

    assert (
        await FileHandler.rename_file(old_file, new_file) is None
    ), "File renaming failed."

    assert not os.path.exists(old_file), f"{old_file} still exists."

    assert os.path.exists(new_file), f"{new_file} was not created."

    os.remove(new_file)
