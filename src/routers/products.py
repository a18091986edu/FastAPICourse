from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, update, desc
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.db_depends import get_async_db, get_db
from src.models.categories import Category as CategoryModel
from src.models.products import Product as ProductModel
from src.models.users import User as UserModel
from src.auth import get_current_seller
from src.schemas import Product as ProductSchema
from src.schemas import ProductCreate, ProductList

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных товаров.
    """
    result = await db.scalars(
        select(ProductModel).where(ProductModel.is_active == True)
    )
    return result.all()

@router.get(
        "/pagination_and_filtration", 
        response_model=ProductList)
async def get_all_products_with_pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=200)] = 20,
    db: AsyncSession = Depends(get_async_db)    
):
    """
    Возвращает список всех активных товаров с пагинацией и фильтрацией
    """
    total_stmt = select(func.count()).select_from(
        ProductModel
    ).where(ProductModel.is_active)

    total = await db.scalar(total_stmt) or 0

    product_stmt = (
        select(ProductModel)
        .where(ProductModel.is_active)
        .order_by(ProductModel.id)
        .offset((page-1)*page_size)
        .limit(page_size)
    )

    items = (await db.scalars(product_stmt)).all()

    return {"items": items, "total": total, "page": page, "size": page_size}


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller)
):
    """
    Создаёт новый товар, привязанный к текущему продавцу (только для 'seller').
    """
    # Проверяем, существует ли активная категория
    category_result = await db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == product.category_id, 
            CategoryModel.is_active
        )
    )
    category = category_result.first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive",
        )

    # Создаём товар
    db_product = ProductModel(**product.model_dump(),
                              seller_id=current_user.id)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_async_db)
):
    """
    Возвращает список активных товаров в указанной категории по её ID.
    """
    # Проверяем, существует ли активная категория
    result = await db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == category_id, 
            CategoryModel.is_active
        )
    )
    category = result.first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or inactive",
        )

    # Получаем активные товары в категории
    product_result = await db.scalars(
        select(ProductModel).where(
            ProductModel.category_id == category_id, 
            ProductModel.is_active
        )
    )
    return product_result.all()


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    # Проверяем, существует ли активный товар
    product_result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, 
            ProductModel.is_active         
        )
    )
    product = product_result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    # Проверяем, существует ли активная категория
    category_result = await db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == product.category_id, 
            CategoryModel.is_active
        )
    )
    category = category_result.first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive",
        )

    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller)
):
    """
    Обновляет товар, если он принадлежит текущему продавцу (только для 'seller').
    """
    # Проверяем, существует ли товар
    db_product = (await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, ProductModel.is_active
        )
    )).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
    if db_product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own products",
        )
    # Проверяем, существует ли активная категория
    category = (await db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == product.category_id, CategoryModel.is_active
        )
    )).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive",
        )

    # Обновляем товар
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**product.model_dump())
    )
    await db.commit()
    await db.refresh(db_product)

    return db_product


@router.delete("/{product_id}", response_model=ProductSchema)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller)
):
    """
    Выполняет мягкое удаление товара, если он принадлежит текущему продавцу (только для 'seller').
    """
    # Проверяем, существует ли активный товар
    product_result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, 
            ProductModel.is_active
        )
    )
    product = product_result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
    if product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own products",
        )

    # Устанавливаем is_active=False
    product.is_active = False
    await db.commit()
    await db.refresh(product)
    return product
