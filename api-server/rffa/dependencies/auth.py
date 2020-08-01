from fastapi import Header

from rffa.applications.auth.access_token import decode_access_token
from rffa.models.user import TokenPayload
from rffa import errors


def access_token(
        authorization=Header(None, description="Bearer ACCESS_TOKEN")
) -> TokenPayload:
    if authorization is None or not authorization.startswith('Bearer '):
        raise errors.InvalidTokenError()

    token = authorization[len('Bearer '):]

    try:
        return decode_access_token(token)
    except BaseException:
        raise errors.InvalidTokenError()
