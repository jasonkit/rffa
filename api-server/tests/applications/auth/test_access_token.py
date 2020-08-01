from rffa.applications.auth.access_token import (
    create_access_token,
    decode_access_token,
)
from rffa.models.user import TokenPayload, UserRole


def test_create_access_token():
    '''
    It should able to create a jwt token for abitary
    payload.
    '''

    token = create_access_token({
        'foo': 'bar'
    })

    assert token


def test_decode_access_token():
    '''
    It should able to get back the TokenPayload.
    '''

    payload = TokenPayload(
        id='some-id',
        username='johndoe',
        role=UserRole.Player,
    )

    token = create_access_token(payload.dict())
    decoded_payload = decode_access_token(token)
    assert decoded_payload == payload
