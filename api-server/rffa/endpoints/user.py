from fastapi import status, Depends
from pydantic import BaseModel, Field

from rffa.app import app
from rffa.models.user import UserSchema
from rffa.applications.user import register, login
from rffa.dependencies.db import db_session
from rffa import errors


class CredentialRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "12345678",
            }
        }


class LoginResponse(BaseModel):
    user: UserSchema
    access_token: str = Field(
        ...,
        description='Access token for API call'
    )

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": "19c22d63-29e8-4bbb-95b5-818cdeea61f9",
                    "username": "johndoe",
                    "last_login_at": None,
                    "profile": {},
                    "role": "player",
                    "is_disabled": False
                },
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImlkIjoiMTljMjJkNjMtMjllOC00YmJiLTk1YjUtODE4Y2RlZWE2MWY5IiwidXNlcm5hbWUiOiJqb2huZG9lIiwicm9sZSI6InBsYXllciJ9LCJleHAiOjE1OTg0MjUxMzcsImlhdCI6MTU5NTgzMzEzN30.8kcA2QJ2o6wt29KBHYCN6u_0d0cnpUEF9uahQxl0UgQ"  # noqa
            }
        }


@app.post(
    '/user',
    description='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=LoginResponse,
    responses=errors.error_responses(
        errors.UsernameAlreadyUsedError,
    )
)
def create_user(
        request: CredentialRequest,
        db_session=Depends(db_session)
):
    user, token = register(db_session, request.username, request.password)
    return LoginResponse(
        user=UserSchema.from_orm(user),
        access_token=token
    )


@app.post(
    '/user/login',
    description='User login',
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses=errors.error_responses(
        errors.InvalidCredentialError,
    )
)
def user_login(
        request: CredentialRequest,
        db_session=Depends(db_session)
):
    user, token = login(db_session, request.username, request.password)
    return LoginResponse(
        user=UserSchema.from_orm(user),
        access_token=token
    )
