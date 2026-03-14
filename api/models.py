from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Numeric, ForeignKey
from typing import Optional,  Annotated

PRODUCT_NAME_LEN = 100

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
class Product(Base):
    __tablename__="products"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(PRODUCT_NAME_LEN),nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True, default="")
    status: Mapped[bool] = mapped_column(default=True)
    
class OrderProduct(Base):
    __tablename__ = "orders_products"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    fk_order_id: Mapped[int] = mapped_column(
         ForeignKey("orders.id")
    )
    quantity: Mapped[int]= mapped_column(
        Integer
    )
    price: Mapped[float] = mapped_column(
        Numeric(10,2)
    )
    