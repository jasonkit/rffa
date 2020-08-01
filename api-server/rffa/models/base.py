from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from rffa.config import config

Base = declarative_base()


def ForeignKey(key):
    return sa.ForeignKey('{}.{}'.format(config.app_name, key))


class BaseMixin:
    __table_args__ = {'schema': config.app_name}

    id = sa.Column('id', sa.Text, primary_key=True)
    created_at = sa.Column('created_at', sa.DateTime, nullable=False)
    updated_at = sa.Column('updated_at', sa.DateTime, nullable=False)

    @staticmethod
    def create_id(mapper, connection, instance):
        if not instance.id:
            instance.id = str(uuid4())

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.now()
        if not instance.created_at:
            instance.created_at = now
        if not instance.updated_at:
            instance.updated_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.now()
        instance.updated_at = now

    @classmethod
    def register(cls):
        sa.event.listen(
            BaseMixin, 'before_insert', cls.create_id, propagate=True)
        sa.event.listen(
            BaseMixin, 'before_insert', cls.create_time, propagate=True)
        sa.event.listen(
            BaseMixin, 'before_update', cls.update_time, propagate=True)


BaseMixin.register()
