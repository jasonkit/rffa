import pytest

from rffa.models.user import UserQuery, UserSchema
from rffa import errors

from tests.utils import (
    check_minimal_request,
    ensure_dict_match_model,
    check_error_response,
)
from tests import fixtures


@pytest.fixture
def crediential():
    return {
        "username": "johndoe",
        "password": "12345678",
    }


@pytest.fixture
def existing_user(context, crediential):
    return context.create_user(
        patch=fixtures.models.minimal_user_data(**crediential),
        need_model=True)


def check_user_schema(payload, user):
    ensure_dict_match_model(
        payload, user,
        keys=[
            'id', 'username', 'last_login_at', 'profile', 'role', 'is_disabled'
        ],
        schema=UserSchema,
    )


def check_login_response(response, user):
    body = response.json()

    check_user_schema(body['user'], user)
    assert body['access_token'] != ""


def test_create_user_minimal_request(context, crediential):
    check_minimal_request(
        lambda x: context.client.post('/user', json=x),
        crediential,
    )

    response = context.client.post('/user', json=crediential)
    assert response.status_code == 201


def test_create_user(context, crediential):
    '''
    Should create a new user, repsonse should
    include user data and access token.
    '''

    response = context.client.post('/user', json=crediential)
    assert response.status_code == 201

    user = UserQuery(context.session).one()
    check_login_response(response, user)


def test_create_user_duplicated_username(context, crediential):
    '''
    Should fail if username is already taken
    '''

    response = context.client.post('/user', json=crediential)
    assert response.status_code == 201

    response = context.client.post('/user', json=crediential)
    check_error_response(response, errors.UsernameAlreadyUsedError())

    assert UserQuery(context.session).count() == 1


def test_user_login(context, existing_user, crediential):
    '''
    Should return user data and access token.
    '''

    response = context.client.post('/user/login', json=crediential)
    assert response.status_code == 200
    check_login_response(response, existing_user)


@pytest.mark.parametrize('credential_patch', [
    {'username': 'non-exists-user'},
    {'password': 'wrong-password'},
])
def test_user_login_with_invalid_credential(
        context, existing_user, crediential, credential_patch):
    '''
    Should fail with invalid credential error
    '''

    response = context.client.post('/user/login', json={
        **crediential,
        **credential_patch,
    })
    check_error_response(response, errors.InvalidCredentialError())
