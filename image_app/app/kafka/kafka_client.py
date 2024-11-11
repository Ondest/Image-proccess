import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()
log = logging.getLogger(__name__)


class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
        self.group_id = settings.KAFKA_GROUP_ID
        self.reply_topic = settings.KAFKA_REPLY_TOPIC
        self.request_topic = settings.KAFKA_REQUEST_TOPIC

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        self.consumer = AIOKafkaConsumer(
            self.request_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
        )

        await self.producer.start()
        log.info("Producer was started")
        await self.consumer.start()
        log.info("Consumer was started")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def send_message(self, message: dict[str, str]) -> None:
        if not self.producer:
            raise Exception("Kafka producer is not started.")

        msg = json.dumps(message)
        await self.producer.send_and_wait(self.reply_topic, msg.encode("utf-8"))
        log.info(f"Message sent to topic {self.reply_topic}: {message}")

    async def listen_for_response(self) -> None:
        if not self.consumer:
            raise Exception("Kafka consumer is not started.")
        log.info("Start listening...")

        async for message in self.consumer:
            log.info(
                f"Message received from topic {self.request_topic}: {message.value}"
            )
            print(self.request_topic, message.value)
            return json.loads(message.value)


kafka_client = KafkaClient(bootstrap_servers=settings.kafka_url)
