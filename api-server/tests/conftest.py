import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from rffa.app import app
from rffa.config import config

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


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
