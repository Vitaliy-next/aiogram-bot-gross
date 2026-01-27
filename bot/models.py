from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, Text, Numeric, String, DateTime, func,ForeignKey
from bot.database import Base
from sqlalchemy import CheckConstraint
from datetime import datetime


class AnnaCos(Base):
    __tablename__ = "annacostest"

    row_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    client_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    client_name: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    products: Mapped[str | None] = mapped_column(Text)
    summ_sale: Mapped[float | None] = mapped_column(Numeric)
    activity: Mapped[str | None] = mapped_column(Text)
    additional_info: Mapped[str | None] = mapped_column(Text)
    period: Mapped[str | None] = mapped_column(Text)


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    file_id: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    media_type: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "media_type IN ('photo', 'video')",
            name="media_type_check"
        ),
    )



class InfoBlock(Base):
    __tablename__ = "info_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )




class StockBlock(Base):
    __tablename__ = "stock_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class PriseBlock(Base):
    __tablename__ = "prise_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class PodiiBlock(Base):
    __tablename__ = "podii_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class ProductBlock(Base):
    __tablename__ = "product_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class NewproductBlock(Base):
    __tablename__ = "newproduct_blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# НОВЫЕ МОДЕЛИ ДЛЯ КОРЗИНЫ КОТОРЫЕ РАБОТАЮТ ПО КОМАНДЕ order
# 1️⃣ МОДЕЛИ БАЗЫ ДАННЫХ (SQLAlchemy2)


# products исправлен

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True)


# users исправлен

class User(Base):
    __tablename__ = "users"

    client_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_name: Mapped[str | None] = mapped_column(Text)
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str | None] = mapped_column(Text)
    contact_phone: Mapped[str | None] = mapped_column(Text)



# ⚠️ client_id, tg_id, client_name, phone
# → берём из annacostest, не дублируем логику

# cart исправлен


class Cart(Base):
    __tablename__ = "cart"

    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    total_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    total_products: Mapped[int | None] = mapped_column(Integer)



# cart_product исправлен

class CartProduct(Base):
    __tablename__ = "cart_product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cart.cart_id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.product_id")
    )
    product_name: Mapped[str] = mapped_column(Text)
    quantity: Mapped[int] = mapped_column(Integer)
    final_price: Mapped[float] = mapped_column(Numeric(10, 2))




# orders исправлен


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int | None] = mapped_column(Integer)
    client_name: Mapped[str | None] = mapped_column(Text)
    tg_id: Mapped[int | None] = mapped_column(BigInteger)
    phone: Mapped[str | None] = mapped_column(Text)
    contact_phone: Mapped[str | None] = mapped_column(Text)
    products_name: Mapped[str | None] = mapped_column(Text)
    total_price: Mapped[float | None] = mapped_column(Numeric(10, 2))

    # status: Mapped[str] = mapped_column(Text, default="paid")  # paid | reserve
    # created_at: Mapped = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(Text, nullable=False, default="paid")  # paid | reserve | pending
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)



