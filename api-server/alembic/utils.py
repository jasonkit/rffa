import sqlalchemy as sa


def common_record_columns():
    return [
        sa.Column('id', sa.Text, unique=True, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    ]
