"""add_content_column_to_post_table

Revision ID: 071ca955d853
Revises: a4b0ad6288da
Create Date: 2022-09-21 16:31:42.040148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '071ca955d853'
down_revision = 'a4b0ad6288da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'Content')
    pass
