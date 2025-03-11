"""Criando tabela bundle

Revision ID: f3641453f666
Revises: 680a5ed13bf3
Create Date: 2025-03-10 18:41:01.401726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3641453f666'
down_revision: Union[str, None] = '680a5ed13bf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=True)
    op.create_table('plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plan_amount'), 'plan', ['amount'], unique=False)
    op.create_index(op.f('ix_plan_description'), 'plan', ['description'], unique=False)
    op.create_index(op.f('ix_plan_id'), 'plan', ['id'], unique=False)
    op.create_index(op.f('ix_plan_name'), 'plan', ['name'], unique=False)
    op.create_index(op.f('ix_plan_plan_id'), 'plan', ['plan_id'], unique=True)
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('recipeType', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_id'), 'session', ['id'], unique=False)
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), server_default='Sem descrição', nullable=False),
    sa.Column('preparation_time', sa.Float(), server_default='0.0', nullable=False),
    sa.Column('serving_size', sa.Integer(), server_default='0', nullable=False),
    sa.Column('dificulty', sa.String(), server_default='Fácil', nullable=False),
    sa.Column('portions', sa.Integer(), server_default='1', nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_id'), 'recipe', ['id'], unique=False)
    op.create_index(op.f('ix_recipe_title'), 'recipe', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_id', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_google_id'), 'user', ['google_id'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_photo_url'), 'user', ['photo_url'], unique=False)
    op.create_table('collection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('icon_name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_id'), 'image', ['id'], unique=False)
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), server_default='Sem descrição', nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ingredient_id'), 'ingredient', ['id'], unique=False)
    op.create_index(op.f('ix_ingredient_title'), 'ingredient', ['title'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_payment', sa.DateTime(), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.Column('payment_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_amount'), 'order', ['amount'], unique=False)
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_table('preparation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('step', sa.Integer(), server_default='0', nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_preparation_id'), 'preparation', ['id'], unique=False)
    op.create_index(op.f('ix_preparation_title'), 'preparation', ['title'], unique=False)
    op.create_table('recipe_categories',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'category_id')
    )
    op.create_table('session_recipe',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'session_id')
    )
    op.create_table('recipe_collection',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'collection_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_collection')
    op.drop_table('session_recipe')
    op.drop_table('recipe_categories')
    op.drop_index(op.f('ix_preparation_title'), table_name='preparation')
    op.drop_index(op.f('ix_preparation_id'), table_name='preparation')
    op.drop_table('preparation')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_index(op.f('ix_order_amount'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_ingredient_title'), table_name='ingredient')
    op.drop_index(op.f('ix_ingredient_id'), table_name='ingredient')
    op.drop_table('ingredient')
    op.drop_index(op.f('ix_image_id'), table_name='image')
    op.drop_table('image')
    op.drop_table('collection')
    op.drop_index(op.f('ix_user_photo_url'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_google_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_recipe_title'), table_name='recipe')
    op.drop_index(op.f('ix_recipe_id'), table_name='recipe')
    op.drop_table('recipe')
    op.drop_index(op.f('ix_session_id'), table_name='session')
    op.drop_table('session')
    op.drop_index(op.f('ix_plan_plan_id'), table_name='plan')
    op.drop_index(op.f('ix_plan_name'), table_name='plan')
    op.drop_index(op.f('ix_plan_id'), table_name='plan')
    op.drop_index(op.f('ix_plan_description'), table_name='plan')
    op.drop_index(op.f('ix_plan_amount'), table_name='plan')
    op.drop_table('plan')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
