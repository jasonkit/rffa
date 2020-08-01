from datetime import datetime
from typing import Tuple

from rffa import errors
from rffa.applications.auth.access_token import create_access_token
from rffa.applications.auth.password import check_password, hash_password
from rffa.models.user import User, UserQuery
from rffa.typing import DBSession


def register(db_session: DBSession,
             username: str, password: str) -> Tuple[User, str]:
    is_username_in_use = (
        UserQuery(db_session)
        .filter_by_username(username)
        .is_exist()
    )

    if is_username_in_use:
        raise errors.UsernameAlreadyUsedError()

    user = User(
        username=username,
        password=hash_password(password),
        last_login_at=datetime.utcnow(),
    )

    db_session.add(user)
    db_session.flush()
    token = create_access_token(user.to_access_token_payload())

    return user, token


def login(db_session: DBSession,
          username: str, password: str) -> Tuple[User, str]:
    user = (
        UserQuery(db_session)
        .filter_by_username(username)
        .first()
    )

    if (
        user is None or
        not check_password(password, user.password)
    ):
        raise errors.InvalidCredentialError()

    user.last_login_at = datetime.utcnow()
    db_session.add(user)
    token = create_access_token(user.to_access_token_payload())

    return user, token
