import logging
import os

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.kafka.kafka_client import kafka_client
from app.services.image_services import delete_image, get_image_by_id

log = logging.getLogger(__name__)


class FileDeleteUseCase:
    def __init__(self, session: AsyncSession, id: int) -> None:
        self.kafka_client = kafka_client
        self.image_id = id
        self.session = session

    async def execute(self) -> None:
        image = await get_image_by_id(self.session, self.image_id)
        if image:
            await delete_image(self.session, self.image_id)
            log.info("Delete image: {}".format(image.file_path))
            os.remove(image.file_path)
            await self.kafka_client.send_message(
                {"message": {"delete": image.file_name}}
            )
        else:
            raise HTTPException(detail="This image does not exists", status_code=404)
