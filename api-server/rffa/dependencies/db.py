from typing import NamedTuple, Optional

from fastapi import Request

from rffa.db import open_session


class DBSessionConfig(NamedTuple):
    is_read_only: bool
    isolation_level: Optional[str] = None


def db_session(request: Request):
    config = DBSessionConfig(False)
    try:
        config = request.state.db_session_config
    except BaseException:
        pass

    with open_session(
            is_read_only=config.is_read_only,
            isolation_level=config.isolation_level,
    ) as session:
        yield session


def use_readonly_session(request: Request):
    request.state.db_session_config = DBSessionConfig(True)


def use_serializable_session(request: Request):
    request.state.db_session_config = DBSessionConfig(
        False,
        isolation_level='SERIALIZABLE')


class config_db_session:
    def __init__(self, config: DBSessionConfig):
        self.config = config

    def __call__(self, request: Request):
        request.state.db_session_config = self.config
