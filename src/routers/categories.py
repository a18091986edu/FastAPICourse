from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.db_depends import get_db, get_async_db
from src.models.categories import Category as CategoryModel
from src.schemas import Category as CategorySchema
from src.schemas import CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: AsyncSession = Depends(get_async_db)):
    """Возвращаем список всех активных категорий"""
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    ressult = await db.scalars(stmt)
    return ressult.all()


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_async_db)):
    """Создёт новую категорию"""
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active
        )
        result = await db.scalars(stmt)
        parent = result.first()
        if parent is None:
            raise HTTPException(detail="Parent category not found", status_code=400)

    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)  # добавляем объект в текущую сессию БД
    await db.commit()  # фиксируем изменения в БД
    await db.refresh(
        db_category
    )  # обновляем объект, чтобы он содержал актуальные данные из БД включая автоматически сгенерированное поле id. Если expire_on_commit = False
    return db_category  # автоматически преобразуется в Pydantic модель благодаря response_model


@router.put("/{category_id}", response_model=CategorySchema, status_code=200)
async def update_category(category_id: int, 
                          category: CategoryCreate, 
                          db: AsyncSession = Depends(get_async_db)):
    """Обновляем категорию по её id"""
    stmt = select(CategoryModel).where(CategoryModel.id == category_id,
                                       CategoryModel.is_active)
    
    result = await db.scalars(stmt)
    db_category = result.first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category.parent_id is not None:
        parent_stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id,
                                                  CategoryModel.is_active)
        result = await db.scalars(parent_stmt)
        parent = result.first()
        if parent is None:
            raise HTTPException(status_code=400, detail="Parent category not found")
        
    update_stmt = (update(CategoryModel)
                   .where(CategoryModel.id == category_id)
                   .values(**category.model_dump(exclude_unset=True)))
    
    # for key, value in product.model_dump(exclude_unset=True).items():
    #     setattr(db_product, key, value) # объект автоматически обновлен в памяти, не нужен refresh

    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=200, response_model=CategorySchema)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    """Лолгически удаляет категорию по id устанавливая is_active=False"""
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active)

    # result = await db.scalars(stmt)
    # category = result.first()

    # category = await db.scalar(stmt)

    category = (await db.scalars(stmt)).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(is_active=False)) # db.scalars не используется, т.ек. update не возвращает объекты модели, а выполняет изменение в БД
    # category.is_active = False
    await db.commit()

    return category


# res = db.execute(
#     update(CategoryModel)
#       .where(CategoryModel.id == category_id, CategoryModel.is_active = True))
#       .values(is_active=False)
#       .returning(CategoryModel.id)  # если БД поддерживает RETURNING (Postgres например)
# )
# updated_id = res.scalar_one_or_none()
# if updated_id is None:
#     raise HTTPException(status_code=404, detail="Category not found")
# db.commit()
# return {"status": "success", "message": "Category marked as inactive"}

