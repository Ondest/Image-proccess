from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class FileTypeError(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid file type. Allowed types: image/jpeg, image/png, image/gif",
    ):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class FileSizeError(HTTPException):
    def __init__(self, detail: str = "File size exceeds the limit of 10MB"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class FileNotFoundError(HTTPException):
    def __init__(self, detail: str = "File not found"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


class FileExistsError(HTTPException):
    def __init__(self, detail: str = "File with this name already exists"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)
