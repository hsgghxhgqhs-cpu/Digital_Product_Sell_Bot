from sqlalchemy import Column, Integer, String, Boolean
from models.user import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_cents = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    link = Column(String, nullable=True)
    text = Column(String, nullable=True)
    is_sold = Column(Boolean, default=False)
    sold_to_user_id = Column(Integer, nullable=True)
    sold_order_id = Column(Integer, nullable=True)