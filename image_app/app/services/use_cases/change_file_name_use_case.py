import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.kafka.kafka_client import KafkaClient, kafka_client
from app.services.file_services import FileHandler
from app.services.image_services import get_image_by_id, update_image_name

log = logging.getLogger(__name__)


class ChangeFileNameUseCase:
    def __init__(self, id: int, name: str, session: AsyncSession) -> None:
        self.kafka_client: KafkaClient = kafka_client
        self.id = id
        self.name = name
        self.session = session

    async def execute(self):
        image = await get_image_by_id(self.session, self.id)
        if not image:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File don't exists"
            )
        new_path = image.file_path.replace(image.file_name, self.name)

        await update_image_name(self.session, self.id, self.name)

        await FileHandler.rename_file(image.file_path, new_path)

        await self.kafka_client.send_message(
            {"message": {"rename": [image.file_path, self.name]}}
        )
