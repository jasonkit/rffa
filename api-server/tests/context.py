from fastapi import Request
from fastapi.testclient import TestClient

from rffa.app import app
from rffa.config import config
from rffa.dependencies import db
from rffa.models.user import User
from tests import fixtures


def mock_db_session_depends(session):
    def db_session_depends(request: Request):
        session_config = db.DBSessionConfig(False)
        try:
            session_config = request.state.db_session_config
        except BaseException:
            pass

        session.begin_nested()
        try:
            session.execute(
                'SET search_path TO {}, public'.format(
                    config.app_name))

            if session_config.is_read_only:
                session.execute('SET TRANSACTION READ ONLY')

            yield session

            if session_config.is_read_only:
                session.rollback()
            else:
                session.commit()

        except:  # noqa
            session.rollback()
            raise

    return db_session_depends


class TestContext:

    def __init__(self, session):
        app.dependency_overrides = {
            db.db_session: mock_db_session_depends(session)
        }

        self.session = session
        self.client = TestClient(app)

    def create_user(self, patch=None, need_model=False):
        user = User(**{
            **fixtures.models.minimal_user_data(),
            **({} if patch is None else patch),
        })
        self.session.add(user)
        self.session.flush()  # for getting user.id
        return user if need_model else user.id

    def create_users(self, count=1, patches=None,
                     need_model=False, index_offset=0):

        user_data_list = (
            [
                fixtures.models.minimal_user_data(
                    'user-{}'.format(i + index_offset))
                for i in range(count)
            ] if patches is None
            else [
                {
                    **fixtures.models.minimal_user_data(
                        'user-{}'.format(i + index_offset)),
                    **patches[i]
                }
                for i in range(len(patches))
            ]
        )

        users = [User(**x) for x in user_data_list]
        self.session.add_all(users)
        self.session.flush()

        return users if need_model else [x.id for x in users]
