from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Project(Base):
    __talename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    employes: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="projects",
        secondary="participations",
        viewonly=True,
        lazy="selectin"
    )

    participant: Mapped[list["Participation"]] = relationship(
        "Participation",
        back_populates="project",
        single_parent=True,
        cascade="all, delete-orphan"
    )

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="employees",
        secondary="participations",
        viewonly=True,
        lazy="selectin"
    )
    participant: Mapped[list["Participation"]] = relationship(
        "Participation",
        back_populates="employee",
        single_parent=True,
        cascade="all, delete-orphan"
    )



class Participation(Base):
    __tablename__ = "participations"
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"),
                                            primary_key=True)
    
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"),
                                             primary_key=True)
    
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    project: Mapped["Project"] = relationship(
        "Project", back_populates="participants"
    )

    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="participants"
    )






















article_tags = Table(
    "article_tags",
    Base.metadata,
    Column(
        "article_id", Integer, ForeignKey("articles.id"), primary_key=True, index=True
    ),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True, index=True),
)

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        back_populates="articles",
        secondary=article_tags,
        lazy="joined",
        uselist=True
    )


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    articles: Mapped[list['Article']] = relationship(
        "Article",
        back_populates="tags",
        secondary=article_tags,
        lazy="joined",
        uselist=True
    )





class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        lazy="joined",
        uselist=True,
        cascade="all, delete-orphan"
    )

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
        uselist=False,
        lazy="joined"
    )



class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    student_number: Mapped[int] = mapped_column(String(20),
                                                unique=True,
                                                nullable=False)
    
    grades: Mapped[list["Grade"]] = relationship(
        "Grade",
        back_populates="student",
        lazy="joined",
        cascade="all, delete-orphan",
        uselist=True
    )
    

class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"),
                                                       nullable=False)
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="grades",
        lazy="joined",
        uselist=False
    )



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
