"""Add loyalty_points to User model

Revision ID: a105eaa05f79
Revises: 93dab3b59393
Create Date: 2024-06-30 15:38:02.795678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a105eaa05f79'
down_revision = '93dab3b59393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loyalty_point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_rating_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('loyalty_points', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('loyalty_points')

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('rating')

    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_rating_timestamp'))

    op.drop_table('rating')
    op.drop_table('loyalty_point')
    # ### end Alembic commands ###
