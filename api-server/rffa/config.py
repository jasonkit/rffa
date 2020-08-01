from pydantic import BaseSettings, PostgresDsn, SecretStr


class Config(BaseSettings):
    database_url: PostgresDsn
    app_name = 'rffa'
    access_token_secret: SecretStr

    log_level = 'INFO'

    class Config:
        case_sensitive = False


config = Config()

__all__ = [
    'config'
]
