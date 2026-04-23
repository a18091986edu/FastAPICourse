from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
from src.db_depends import get_db
from src.models.categories import Category as CategoryModel
from src.models.products import Product as ProductModel
from src.schemas import Product as ProductSchema, ProductCreate



router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductSchema], status_code=200)
async def get_all_products(db: Session = Depends(get_db)):
    """Возвращает список всех товаров"""
    return db.scalars(select(ProductModel).join(CategoryModel)
                      .where(ProductModel.is_active,
                             CategoryModel.is_active,
                             ProductModel.stock > 0)).all()



@router.post("/", response_model=ProductSchema, status_code=201)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Создвает новый товар"""
    category = db.scalars(
        select(CategoryModel).where(
            product.category_id == CategoryModel.id, CategoryModel.is_active
        )
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive",
        )

    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/category/{category_id}", 
            response_model=list[ProductSchema])
async def get_products_by_category(category_id: int,
                                   db: Session = Depends(get_db)):
    """Возвращает список активнх товаров в указанной категории по её id"""
    category = db.scalars(select(CategoryModel)
                          .where(CategoryModel.id == category_id,
                                 CategoryModel.is_active)).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found or inactive")
    
    products = db.scalars(
        select(ProductModel).where(
            ProductModel.category_id == category_id,
            ProductModel.is_active)
    ).all()

    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Возвращает детальну информацию о товаре по его ID"""
    try:
        product = db.scalars(
            select(ProductModel)
            .where(ProductModel.id == product_id,
                ProductModel.is_active)
        ).one_or_none()
    except MultipleResultsFound:
        raise HTTPException(detail="Найдено несколько товаров с указанным id", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    category = db.scalars(
        select(CategoryModel)
        .where(CategoryModel.id == product.category_id,
               CategoryModel.is_active)
    ).first()
    if not category:
        raise HTTPException(detail="Category not found or inactive",
                            status_code=400)
    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    """
    Обновляет товар по его ID.
    """
    # Проверяем, существует ли товар
    db_product = db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, 
            ProductModel.is_active
        )
    ).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    # Проверяем, существует ли активная категория
    category = db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == product.category_id, 
            CategoryModel.is_active
        )
    ).first()
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
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаляет товар по его ID (логическое удаление).
    """
    # Проверяем, существует ли активный товар
    product = db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, ProductModel.is_active
        )
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    # Изменяем объект установив is_active=False и сохраняем
    product.is_active = False
    db.commit()

    return {"status": "success", "message": "Product marked as inactive"}
