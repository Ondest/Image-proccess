import logging
import os
from pathlib import Path
import shutil

from PIL import Image, ImageOps


logger = logging.getLogger(__name__)


async def resize_image(file_name, path):
    try:
        with Image.open(path) as img:
            resized_100_100 = img.resize((100, 100))
            resized_300_300 = img.resize((300, 300))

            resized_300_300.save(f"static/resized/300x300_{file_name}")
            resized_100_100.save(f"static/resized/100x100_{file_name}")
            logger.info("Image {} was resized to 100x100 and 300x300".format(file_name))

    except Exception as e:
        logger.error("Error was occured with {}: {}".format(file_name, e))


async def greyscale_image(file_name, path):
    try:
        with Image.open(path) as img:
            resolution = img.size
            new_file_name = f"grayscale_{file_name}"

            grayscale = ImageOps.grayscale(img)
            grayscale.save(f"static/greyscale/{new_file_name}")
            logger.info(
                "Grayscale file version of {}: {}".format(file_name, new_file_name)
            )

        return resolution
    except Exception as e:
        logger.error("Error was occured with {}: {}".format(file_name, e))


async def delete_images(file_name):
    logger.info("Delete request was accepted for {}".format(file_name))
    for file in Path().rglob("*"):
        if file_name in file.name:
            os.remove(file)
            logger.info("{} was deleted".format(file))


async def rename_images(file_names):
    logger.info("Rename request was accepted for {}".format(file_names[0]))
    for file in Path().rglob("*"):
        if file_names[0] in file.name:
            old_path = Path(file)
            suffix = old_path.suffix
            new_path = Path(file_names[1]).with_suffix(suffix)
            shutil.move(old_path, new_path)
            logger.info("{} was renamed to {}".format(old_path.name, new_path.name))
