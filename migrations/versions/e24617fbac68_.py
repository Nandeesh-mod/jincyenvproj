"""empty message

Revision ID: e24617fbac68
Revises: f6054ef7a868
Create Date: 2025-03-10 10:50:56.099574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e24617fbac68'
down_revision = 'f6054ef7a868'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('location_url', sa.String(length=255), nullable=True),
    sa.Column('severity', sa.String(length=20), nullable=False),
    sa.Column('problem_types', sa.Text(), nullable=False),
    sa.Column('image_names', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complaints')
    # ### end Alembic commands ###
