from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    size: int
    resolution: str


class UploadSchema(BaseModel):
    message: str = "Image was upload succesfully"

    file_path: str
    file_name: str
    size: int
    uploaded_at: datetime = datetime.now()
    resolution: str = ""
