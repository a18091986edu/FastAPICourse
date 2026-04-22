from decimal import Decimal
from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)
    
    name: Mapped[str] = mapped_column(String(100),
                                      nullable=False)
    
    email: Mapped[str] = mapped_column(String(120),
                                       unique=True,
                                       nullable=False)
    
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="product",
        uselist=True,
        cascade="all, delete-orphan",
        lazy="joined",
    )



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True)
    
    order_number: Mapped[str] = mapped_column(String(20),
                                              unique=True,
                                              nullable=False)
    
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10,2),
                                                  nullable=False) 
    
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"),
                                             nullable=False)
    
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="orders",
        uselist=False,
        lazy="joined"
    )

























class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=True
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10,2), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        unique=True,
        nullable=False
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )

























class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), 
                                          unique=True, 
                                          nullable=False)
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         unique=True)
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile"
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="author", cascade="all, delete-orphan", lazy="joined"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), nullable=False, unique=True
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
