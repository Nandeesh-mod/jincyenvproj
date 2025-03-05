"""added First name

Revision ID: 327714e4af26
Revises: 700696f5a8f3
Create Date: 2025-03-05 04:55:26.810466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327714e4af26'
down_revision = '700696f5a8f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###
