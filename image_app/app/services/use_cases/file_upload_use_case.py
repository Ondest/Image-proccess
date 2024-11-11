from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.kafka.kafka_client import kafka_client
from app.services.file_services import FileHandler, STATIC_DIR
from app.services.image_services import add_new_image


class FileUploadUseCase:
    def __init__(self, file_obj: UploadFile, session_dependency: AsyncSession) -> None:
        self.kafka_client = kafka_client
        self.file_obj = file_obj
        self.session_dependency = session_dependency

    async def execute(self):
        file_proccess = await FileHandler.save_file(self.file_obj, STATIC_DIR)

        await self.kafka_client.send_message(
            {"message": {"proccess": file_proccess.file_name}}
        )
        response = await self.kafka_client.listen_for_response()

        file_proccess.resolution = (
            f"{response['resolution'][0]}*{response['resolution'][1]}"
        )
        await add_new_image(
            session=self.session_dependency,
            file_name=file_proccess.file_name,
            file_path=file_proccess.file_path,
            size=file_proccess.size,
            resolution=file_proccess.resolution,
        )
        return file_proccess
