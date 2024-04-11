"""add order_id to orderinfo

Revision ID: 839d2d683d87
Revises: 334053fab3c9
Create Date: 2024-04-11 21:51:53.821344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '839d2d683d87'
down_revision = '334053fab3c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_information', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'order', ['order_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_information', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('order_id')

    # ### end Alembic commands ###