from pydantic import BaseModel, EmailStr, ConfigDict


class TokenInfo(BaseModel):
    access_token: str
    token_type: str

# Валидация пользователя по токену
class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None

class Payload(BaseModel):
    sub: str
    email: EmailStr | None = None
