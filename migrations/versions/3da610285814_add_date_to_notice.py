"""Add date to Notice

Revision ID: 3da610285814
Revises: 48ca0c401780
Create Date: 2024-11-24 14:10:28.416939

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3da610285814'
down_revision = '48ca0c401780'
branch_labels = None
depends_on = None

def upgrade():
    # Provide a default value for existing rows
    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.String(length=50), nullable=False, server_default='1970-01-01'))

    # Remove the server default after the column is created
    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.alter_column('date', server_default=None)

def downgrade():
    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.drop_column('date')
