from datetime import datetime, timedelta

import bcrypt
from fastapi import Form, HTTPException, status
import jwt

from app.core.config import settings
from app.db.redis_client import oauth2_client


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await oauth2_client.get_user(username)):
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=bytes(user["password"], encoding="utf-8"),
    ):
        raise unauthed_exc

    return user


def encode_jwt(
    payload: dict[str, str],
    private_key: str = settings.JWT.private_key.read_text(),
    algorithm: str = settings.JWT.algorithm,
    expire_minutes: int = settings.JWT.expire,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.JWT.public_key.read_text(),
    algorithm: str = settings.JWT.algorithm,
) -> dict[str, str]:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
