from sqlalchemy import Table, Column, ForeignKey
from app.database.config import Base
user_product = Table(
    'user_product',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True,index=True),
    Column('product_id', ForeignKey('product.id'), primary_key=True,index=True)
)
