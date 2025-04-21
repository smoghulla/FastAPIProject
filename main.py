import decimal
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, condecimal, conint, validator
from typing import Annotated, List, Optional

from sqlalchemy import desc, asc

import models

from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session, Query

from enum import Enum

app = FastAPI()
#models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class ProductBase(BaseModel):
    product_name: str
    cost: condecimal(max_digits=10, decimal_places=2)
    description: str

class OrderBase(BaseModel):
    product_id: int
    user_id: int
    quantity: Optional[conint(ge=1, strict=True)] = 1

    @validator("quantity")
    def quantity_non_nullable(cls, value):
        assert value is not None, "quantity may not be None"
        return value

class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"

class OrderStatusBase(BaseModel):
    order_id: int
    order_status: StatusEnum

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db:db_dependency):
    db_user = models.User(**user.dict())
    user = db.query(models.User).filter_by(email=db_user.email).first()
    if user:
        raise HTTPException(status_code=409, detail="Email already registered")
    else:
        db.add(db_user)
        db.commit()
        return db_user.id

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, db:db_dependency):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    return db_product.id

@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db:db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products", status_code=status.HTTP_200_OK)
async def get_product(db:db_dependency):
    products = db.query(models.Product).limit(10).all()
    if products is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderBase, db:db_dependency):
    db_order = models.Order(**order.dict())
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    product = db.query(models.Product).filter(models.Product.id == db_order.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    elif user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db_order.cost = product.cost
        db_order.total_amount = db_order.quantity * product.cost
        db.add(db_order)
        db.commit()
        db_order_status = models.OrderStatus()
        db_order_status.order_id = db_order.id
        db_order_status.order_status = StatusEnum.created.value
        db.add(db_order_status)
        db.commit()

@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db:db_dependency):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders/status", status_code=status.HTTP_201_CREATED)
async def create_order_status(status: OrderStatusBase, db:db_dependency):
    order = db.query(models.Order).filter(models.Order.id == status.order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        db_order_status = models.OrderStatus()
        db_order_status.order_id = order.id
        db_order_status.order_status = status.order_status.value
        db.add(db_order_status)
        db.commit()

@app.get("/orders/status/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int, db:db_dependency):
    order_status = db.query(models.OrderStatus).filter(models.OrderStatus.order_id == order_id).order_by(models.OrderStatus.status_update_time.desc()).first()
    if order_status is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_status