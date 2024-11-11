from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr

from app.core.security import decode_jwt, encode_jwt, hash_password, validate_auth_user
from app.db.redis_client import oauth2_client
from app.schemas.auth import Payload, TokenInfo, UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


router = APIRouter()


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> Payload:
    try:
        payload = Payload(
            **decode_jwt(
                token=token,
            )
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: Payload = Depends(get_current_token_payload),
) -> UserSchema:
    username: str = payload.sub
    if user := await oauth2_client.get_user(username=username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


@router.post("/login/")
def auth_user_jwt(
    user: dict[str, str] = Depends(validate_auth_user),
) -> TokenInfo:
    jwt_payload = {
        "sub": user["username"],
        "email": user["email"],
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.post("/users/add/", status_code=201)
async def add_user(
    username: str = Form(...),
    password: str = Form(...),
    email: EmailStr = Form(...),
) -> dict[str, str]:
    if await oauth2_client.user_exists(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    hashed_password = hash_password(password)

    await oauth2_client.set_user(
        username=username, password=hashed_password, email=email
    )

    return {"msg": f"User {username} added successfully."}
