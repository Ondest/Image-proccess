from dataclasses import dataclass
import logging

from dotenv import dotenv_values


@dataclass
class Config:
    KAFKA_URL: str
    REQUEST_TOPIC: str
    REPLY_TOPIC: str


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


settings = Config(**dotenv_values(".env"))
