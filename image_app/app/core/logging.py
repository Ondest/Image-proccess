import logging

from .config import settings


def configure_logging():
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )
