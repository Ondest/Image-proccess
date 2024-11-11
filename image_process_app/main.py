import asyncio
import json
import logging
from pathlib import Path

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from common import configure_logging, settings
from image_handler import delete_images, greyscale_image, rename_images, resize_image

logger = logging.getLogger(__name__)


async def read_requests():
    consumer = AIOKafkaConsumer(
        settings.REQUEST_TOPIC,
        bootstrap_servers=settings.KAFKA_URL,
        group_id="image-process-group",
    )
    await consumer.start()

    try:
        async for msg in consumer:
            task: dict = json.loads(msg.value)["message"]
            match task:
                case {"proccess": _}:
                    await proccess_image(task["proccess"])
                case {"delete": _}:
                    await delete_images(task["delete"])
                case {"rename": [_, _]}:
                    await rename_images(task["rename"])
                case _:
                    logger.warning("Message was unhandled.\nContent: {}".format(task))
    finally:
        await consumer.stop()


async def send_to_topic(topic, message):
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    await producer.start()
    try:
        await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))
    finally:
        await producer.stop()


async def proccess_image(file_name):
    logger.info(
        "Message was delivered for image proccess service!\nFilename: {}".format(
            file_name
        )
    )
    path = Path(f"static/images/{file_name}")

    if not path.exists():
        raise FileNotFoundError()

    resolution = await greyscale_image(file_name, path)
    await resize_image(file_name, path)

    await send_to_topic(
        settings.REPLY_TOPIC,
        {"message": "Grayscale process was done!", "resolution": resolution},
    )
    logger.info(
        "Message sent from image_proccess_app in {}".format(settings.REPLY_TOPIC)
    )


if __name__ == "__main__":
    configure_logging()
    logger.info("Image service was started!!!")
    asyncio.run(read_requests())
