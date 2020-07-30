from typing import Dict
from datetime import timedelta, datetime

import jwt

from rffa.models.user import TokenPayload
from rffa.config import config


def create_access_token(
        payload: Dict,
        expire_after=timedelta(days=30),
):

    content = {'payload': payload}
    if expire_after is not None:
        content['exp'] = int(  # type: ignore
            (datetime.utcnow() + expire_after).timestamp())

    content['iat'] = int(datetime.utcnow().timestamp())  # type: ignore

    return jwt.encode(
        content,
        config.access_token_secret.get_secret_value(),
        algorithm='HS256',
    )


def decode_access_token(token: str) -> TokenPayload:
    content = jwt.decode(
        token,
        config.access_token_secret.get_secret_value(),
        algorithms='HS256',
        options={
            'require_iat': True,
            'verify_iat': True,
            'verify_exp': True,
            'verify_signature': True,
        }
    )
    return TokenPayload(**content['payload'])
