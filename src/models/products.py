from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    img_url: Mapped[str] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# if __name__ == "__main__":
#     from sqlalchemy.schema import CreateTable
#     from src.models.categories import Category
#     print(CreateTable(Category.__table__))
#     print(CreateTable(Product.__table__))


