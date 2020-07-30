import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
