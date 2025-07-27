from sqlalchemy import Integer, Table, Column, ForeignKey
from app.database.config import Base
product_item = Table(
    'product_item',
    Base.metadata,
    Column('product_id', ForeignKey('product.id'), primary_key=True,index=True),
    Column('item_id', Integer, primary_key=True, index=True)
)
