from datetime import datetime

from rffa.models.user import (
    User,
    UserQuery,
    UserRole
)


def test_create_user(db_session):

    start_at = datetime.utcnow()

    user_data = {
        'username': 'johndoe',
        'password': 'password',
    }

    user = User(**user_data)
    db_session.add(user)
    db_session.flush()

    user = UserQuery(db_session).one()

    assert user.id is not None

    for key, value in user_data.items():
        assert getattr(user, key) == value

    assert user.created_at > start_at
    assert user.updated_at > start_at
    assert user.role == UserRole.Player
    assert user.profile == {}
    assert not user.is_disabled
