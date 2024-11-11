from io import BytesIO
from sqlalchemy import insert
from app.core.config import settings
from app.api.main import app as main_app
from app.db.base import Base
from app.db.models import Image
from app.db.database import db_handler
from httpx import AsyncClient
from fastapi import UploadFile
from starlette.datastructures import Headers
import pathlib

import pytest
import asyncio
import json
import shutil

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    await db_handler._init_tests_db(settings.test_db_url)
    assert str(db_handler.engine.url).endswith(settings.TEST_DB)

    async with db_handler.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with db_handler.session_factory() as session:
        path = pathlib.Path("tests/mock_data/images.json").absolute()
        with open(path, "r") as file:
            test_images_data = json.load(file)
            stmt = insert(Image).values(test_images_data)
            await session.execute(stmt)
            await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def prepare_redis():
    pool = ConnectionPool.from_url(url=settings.redis_url)
    r = redis.Redis(connection_pool=pool)
    await r.flushall()
    FastAPICache.init(RedisBackend(r), prefix="test-cache")
    yield


@pytest.fixture(scope="session")
def event_loop():
    asyncio.get_event_loop_policy().set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def a_client():
    async with AsyncClient(app=main_app, base_url="http://test") as a_client:
        yield a_client


@pytest.fixture(scope="session")
def file_upload():
    file_content = b"Test content"
    file = UploadFile(
        file=BytesIO(file_content),
        headers=Headers({"content_type": "image/jpeg"}),
    )
    yield file


@pytest.fixture(scope="session")
def temp_dir_for_tests(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = tmpdir_factory.mktemp("test_files")
    yield temp_dir
    shutil.rmtree(str(temp_dir), ignore_errors=True)


@pytest.fixture(scope="function")
async def session_dependency():
    async with db_handler.session_factory() as session:
        yield session
