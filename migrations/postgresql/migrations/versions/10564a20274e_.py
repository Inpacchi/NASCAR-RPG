"""empty message

Revision ID: 10564a20274e
Revises: 0f7ff653b7a5
Create Date: 2019-10-28 16:58:47.171600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10564a20274e'
down_revision = '0f7ff653b7a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('equipment_rented_from', sa.Integer(), nullable=True))
    op.add_column('team', sa.Column('notes', sa.String(length=128), nullable=True))
    op.create_foreign_key(None, 'team', 'team', ['equipment_rented_from'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'team', type_='foreignkey')
    op.drop_column('team', 'notes')
    op.drop_column('team', 'equipment_rented_from')
    # ### end Alembic commands ###