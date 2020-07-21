import logging

from rffa.config import config

logging.basicConfig(level=config.log_level)
logger = logging.getLogger('rffa')

__all__ = [
    'logger'
]
