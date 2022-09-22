"""add forign_key to posts table

Revision ID: 011a9395a30d
Revises: c0c4c48703cc
Create Date: 2022-09-21 17:13:54.849399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '011a9395a30d'
down_revision = 'c0c4c48703cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts",
    referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
