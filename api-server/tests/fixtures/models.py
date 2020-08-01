from datetime import datetime

from rffa.applications.auth.password import hash_password


def minimal_user_data(username='johndoe', password='12345678'):
    return {
        'username': username,
        'password': hash_password(password),
        'last_login_at': datetime.utcnow(),
    }
