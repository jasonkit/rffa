import os

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from rffa.config import config
from tests.context import TestContext

ENGINE = create_engine(os.getenv('TEST_DATABASE_URL'))
SESSION = sessionmaker()


@pytest.fixture()
def db_session():

    # Adapted from
    # https://docs.sqlalchemy.org/en/13/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites

    connection = ENGINE.connect()
    transaction = connection.begin()
    session = SESSION(bind=connection)
    session.execute(
        'SET search_path TO {}, public'.format(config.app_name))

    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    yield session

    # To suppress warning, probably could remove after sqlalchemy
    # release 1.3.19, ref:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5361#issuecomment-636121385
    connection.connection._reset_agent = None

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def context(db_session):
    return TestContext(db_session)
