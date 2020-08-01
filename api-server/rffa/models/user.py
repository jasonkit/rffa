import json
from datetime import datetime
from enum import Enum
from typing import Any

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base, BaseMixin
from .base_query import BaseQuery


class UserRole(str, Enum):
    Player = 'player'


class User(Base, BaseMixin):
    __tablename__ = 'user'
    username = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)
    last_login_at = sa.Column(sa.DateTime, nullable=False)
    role = sa.Column(sa.Enum(UserRole), nullable=False,
                     default=UserRole.Player)
    profile = sa.Column(JSONB, nullable=False, default={})
    is_disabled = sa.Column(sa.Boolean, nullable=False, default=False)

    def to_access_token_payload(self):
        return json.loads(TokenPayload.from_orm(self).json())


class TokenPayload(BaseModel):
    id: str
    username: str
    role: UserRole

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: str
    username: str
    last_login_at: datetime
    profile: Any
    role: UserRole
    is_disabled: bool

    class Config:
        orm_mode = True


class UserQuery(BaseQuery):
    def __init__(self, session):
        super().__init__(session, User)

    def filter_by_username(self, username):
        self.query = self.query.filter(User.username == username)
        return self

    def filter_by_password(self, password):
        self.query = self.query.filter(User.password == password)
        return self
