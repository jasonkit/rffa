"""create user table

Revision ID: 8c18318c26a5
Revises:
Create Date: 2020-07-26 09:56:04.248974

"""
from alembic import op
import sqlalchemy as sa
import os

from importlib.machinery import SourceFileLoader
SourceFileLoader('alembic_utils', './alembic/utils.py').load_module()


# revision identifiers, used by Alembic.
revision = '8c18318c26a5'
down_revision = None
branch_labels = None
depends_on = None

SCHEMA_NAME = os.getenv('APP_NAME')


def upgrade():
    from alembic_utils import common_record_columns

    op.create_table(
        'user',
        *common_record_columns(),
        sa.Column('username', sa.Text, unique=True, nullable=False),
        sa.Column('password', sa.Text, nullable=False),
        sa.Column('last_login_at', sa.DateTime, nullable=False),
        sa.Column('role', sa.Text, nullable=False,
                  server_default='player'),
        sa.Column('profile', sa.dialects.postgresql.JSONB, nullable=False,
                  server_default='{}'),
        sa.Column('is_disabled', sa.Boolean, nullable=False,
                  server_default='false'),
        schema=SCHEMA_NAME,
    )

    op.create_index('idx_user_username', 'user', ['username'],
                    schema=SCHEMA_NAME)


def downgrade():
    op.drop_index('idx_user_username', 'user', schema=SCHEMA_NAME)
    op.drop_table('user', schema=SCHEMA_NAME)
