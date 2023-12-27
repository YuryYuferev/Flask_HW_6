# Cоздать на python базу данных для интернет-магазина.
# База данных должна состоять из трех таблиц: товары, заказы и пользователи.
# Таблица товары должна содержать информацию о доступных товарах, их описаниях и ценах.
# Таблица пользователи должна содержать информацию о зарегистрированных пользователях магазина.
# Таблица заказы должна содержать информацию о заказах, сделанных пользователями.
# Таблица пользователей должна содержать поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
# Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей). Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API
# (итого 15 маршрутов).-Чтение всех, -Чтение одного, -Запись, -Изменение, -Удаление.


from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

DATABASE_URL = "sqlite:///./internet_shop.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    order_date = Column(DateTime)
    status = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float

class ItemRead(BaseModel):
    id: int
    name: str
    description: str
    price: float

class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    order_date: datetime
    status: str

class OrderRead(BaseModel):
    id: int
    user: UserRead
    item: ItemRead
    order_date: datetime
    status: str

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

@app.post("/items/", response_model=ItemRead)
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemCreate):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

@app.post("/orders/", response_model=OrderRead)
def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = Order(user_id=order.user_id, item_id=order.item_id, order_date=order.order_date, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderRead)
def read_order(order_id: int):
    db = SessionLocal()
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order: OrderCreate):
    db = SessionLocal()
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.user_id = order.user_id
    db_order.item_id = order.item_id
    db_order.order_date = order.order_date
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    db = SessionLocal()
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted"}

# uvicorn Task6:app --reload
