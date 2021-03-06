"""secord migration relation

Revision ID: 96a90d9316e6
Revises: 68bddc917ca7
Create Date: 2022-07-18 15:20:35.154562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96a90d9316e6'
down_revision = '68bddc917ca7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tag_id', 'todo_id')
    )
    op.add_column('todo', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('todo', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todo', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todo', type_='foreignkey')
    op.drop_column('todo', 'user_id')
    op.drop_column('todo', 'active')
    op.drop_table('tags')
    op.drop_table('tag')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
