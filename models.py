from sqlalchemy import Boolean, String, Column, Integer, DECIMAL, ForeignKey, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(50))
    cost = Column(DECIMAL(10,2))
    description = Column(String(255))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    cost = Column(DECIMAL(10,2))
    quantity = Column(Integer)
    total_amount = Column(DECIMAL(10,2))
    user_id = Column(Integer, ForeignKey("users.id"))

class OrderStatus(Base):
    __tablename__ = "order_statuses"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order_status = Column(String(20))
    status_update_time = Column(DateTime, default=datetime.now)

