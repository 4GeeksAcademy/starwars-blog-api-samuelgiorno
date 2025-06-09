"""empty message

Revision ID: ea3296e3f6cb
Revises: a5cffa318ac2
Create Date: 2025-06-04 18:45:31.185209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea3296e3f6cb'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('planets',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=400), nullable=False),
                    sa.Column('description', sa.String(
                        length=120), nullable=False),
                    sa.Column('galaxy', sa.String(length=120), nullable=False),
                    sa.Column('population', sa.String(
                        length=120), nullable=False),
                    sa.Column('gravity', sa.Integer(), nullable=False),
                    sa.Column('image', sa.String(length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('favourite_planet',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('planet_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('people',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=400), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=False),
                    sa.Column('gender', sa.String(length=120), nullable=False),
                    sa.Column('height', sa.Integer(), nullable=False),
                    sa.Column('weight', sa.Integer(), nullable=False),
                    sa.Column('image', sa.String(length=120), nullable=False),
                    sa.Column('planet_of_birth', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['planet_of_birth'], ['planets.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('favourite_people',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('people_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('favourite_people')
    op.drop_table('people')
    op.drop_table('favourite_planet')
    op.drop_table('planets')
