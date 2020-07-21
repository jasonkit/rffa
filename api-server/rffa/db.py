from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rffa.config import config

ENGINE = create_engine(config.database_url)
SESSION = sessionmaker()
SESSION.configure(bind=ENGINE)


@contextmanager
def open_session(is_read_only=False, isolation_level=None):
    session = SESSION(
        bind=(
            ENGINE if isolation_level is None
            else ENGINE.execution_options(isolation_level=isolation_level)
        ))

    try:
        session.execute(
            'SET search_path TO {}, public'.format(
                config.app_name))

        if is_read_only:
            session.execute('SET TRANSACTION READ ONLY')

        yield session

        if is_read_only:
            session.rollback()
        else:
            session.commit()
    except:  # noqa
        session.rollback()
        raise
    finally:
        session.close()
