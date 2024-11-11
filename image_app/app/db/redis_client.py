import json

from redis.asyncio import Redis

from app.core.config import settings
from app.schemas.auth import UserSchema


class RedisOAuth2Client:
    def __init__(self, redis_client) -> None:
        self.redis = redis_client

    async def set_user(self, username: str, password: bytes, email: str) -> None:
        user_data = {
            "username": username,
            "password": password,
            "email": email,
        }
        user = UserSchema(**user_data)  # type: ignore
        await self.redis.set(f"user:{username}", user.model_dump_json())

    async def get_user(self, username: str) -> UserSchema | None:
        data = await self.redis.get(f"user:{username}")
        if data:
            return json.loads(data)
        return None

    async def user_exists(self, username: str) -> bool:
        data = await self.redis.get(f"user:{username}")
        return data is not None


redis = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
)
oauth2_client = RedisOAuth2Client(redis)
