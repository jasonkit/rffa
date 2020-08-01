import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rffa.config import config
from tests.context import TestContext

ENGINE = create_engine(os.getenv('TEST_DATABASE_URL'))
SESSION = sessionmaker()
SESSION.configure(bind=ENGINE)


@pytest.fixture()
def db_session():
    session = SESSION()
    session.execute(
        'SET search_path TO {}, public'.format(config.app_name))

    yield session

    session.rollback()
    session.close()


@pytest.fixture()
def context(db_session):
    return TestContext(db_session)
