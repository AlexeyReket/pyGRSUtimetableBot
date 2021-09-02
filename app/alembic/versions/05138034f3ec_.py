"""empty message

Revision ID: 05138034f3ec
Revises: 
Create Date: 2021-08-30 13:54:16.504431

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05138034f3ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comics',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.PrimaryKeyConstraint('id', 'date')
                    )
    op.create_table('courses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('num', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('faculties',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('forms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('chat_id', sa.Integer(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('role', sa.Integer(), nullable=True),
                    sa.Column('get_comics', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('groups',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('faculty_id', sa.Integer(), nullable=True),
                    sa.Column('course_id', sa.Integer(), nullable=True),
                    sa.Column('form_id', sa.Integer(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=False),
                    sa.Column('status_name', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
                    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('groups_link_users',
                    sa.Column('group_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('group_id', 'user_id')
                    )
    op.create_table('timetables',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('schedule', sa.JSON(), nullable=True),
                    sa.Column('group_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timetables')
    op.drop_table('groups_link_users')
    op.drop_table('groups')
    op.drop_table('users')
    op.drop_table('forms')
    op.drop_table('faculties')
    op.drop_table('courses')
    op.drop_table('comics')
    # ### end Alembic commands ###
