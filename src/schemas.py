from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryCreate(BaseModel):
    """Модель для создания и обновления категории. Испольуется в POST и PUT"""

    name: Annotated[
        str,
        Field(
            ...,
            min_length=3,
            max_length=50,
            description="Название категории (3-50 символов)",
        ),
    ]

    parent_id: Annotated[
        int | None,
        Field(description="ID родительской категории, если есть"),
    ] = None


class Category(CategoryCreate):
    """Модель для ответа с данными о категории. Используется в GET"""

    id: Annotated[int, Field(..., description="Уникальный идетификатор категории")]
    is_active: Annotated[
        bool | None, Field(description="ID категории, если есть")
    ] = None

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """Модель для создания и обновления товара. Используется в POST и PUT"""

    name: Annotated[
        str,
        Field(
            ...,
            min_length=3,
            max_length=100,
            description="Описание товара (3-100 символов)",
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            max_length=500,
            description="Описание товара (до 500 символов)",
        ),
    ] = None
    price: Annotated[
        Decimal,
        Field(..., gt=0, description="Цена товара (больше 0)", decimal_places=2),
    ]
    img_url: Annotated[
        str | None, Field(max_length=200, description="URL изображения товара")
    ] = None
    stock: Annotated[
        int, Field(..., ge=0, description="Количество товара на складе (0 или больше)")
    ]
    category_id: Annotated[
        int, Field(..., description="ID категории, к которой относится товар")
    ]


class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор товара")]

    name: Annotated[str, Field(description="Название товара")]

    description: Annotated[str | None, Field(description="Описание товара")] = None

    price: Annotated[
        Decimal, Field(gt=0, description="Цена товара в рублях", decimal_places=2)
    ]

    image_url: Annotated[str | None, Field(description="URL изображения товара")] = None

    stock: Annotated[int, Field(description="Количество товара на складе")]

    category_id: Annotated[int, Field(description="ID категории")]

    is_active: Annotated[bool, Field(description="Активность товара")]

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """
    Список пагинации для товаров
    """
    items: Annotated[list[Product], 
                     Field(
                         description="Товары для текущей страницы")]
    total: Annotated[
        int, 
        Field(ge=0, description="Общее количество товаров")
    ]

    page: Annotated[
        int,
        Field(ge=1, description="Номер текущей страницы")
    ]

    page_size: Annotated[
        int, 
        Field(ge=1, description="Количество элементов на странице")
    ]

    model_config = ConfigDict(from_attributes=True)



class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(..., description="Уникальный email пользователя")]
    password: Annotated[str, Field(
        ..., description="Пароль пользователя"
    )]
    role: Annotated[
        str,
        Field(
            default="buyer",
            pattern="^(buyer|seller)$",
            description="Роль: 'buyer' или 'seller'",
        ),
    ]
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: Annotated[int, 
                  Field(...,
                      description=
                      "Уникальный идентификатор пользователя")]
    is_active: Annotated[bool, Field(..., description="Активность пользователя")]

    


