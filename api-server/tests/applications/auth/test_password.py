from rffa.applications.auth.password import check_password, hash_password


def test_hash_password():
    '''
    It should return a hashed password.
    '''

    password = 'password'
    assert hash_password(password) != password


def test_check_password():
    '''
    It should able to check password against the hashed password.
    '''

    password = 'password'
    assert check_password(password, hash_password(password))
