"""empty message

Revision ID: 4a9b1edc5985
Revises: a0748f1b3989
Create Date: 2021-08-17 17:11:42.550476

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4a9b1edc5985'
down_revision = 'a0748f1b3989'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=80),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###