from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.db_depends import get_db
from src.models.categories import Category as CategoryModel
from src.schemas import Category as CategorySchema
from src.schemas import CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: Session = Depends(get_db)):
    """Возвращаем список всех активных категорий"""
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    return db.scalars(stmt).all()


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создёт новую категорию"""
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active
        )
        parent = db.scalars(stmt).first()
        if parent is None:
            raise HTTPException(detail="Parent category not found", status_code=400)

    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)  # добавляем объект в текущую сессию БД
    db.commit()  # фиксируем изменения в БД
    db.refresh(
        db_category
    )  # обновляем объект, чтобы он содержал актуальные данные из БД включая автоматически сгенерированное поле id
    return db_category  # автоматически преобразуется в Pydantic модель благодаря response_model


@router.put("/{category_id}", response_model=CategorySchema, status_code=200)
async def update_category(category_id: int, 
                          category: CategoryCreate, 
                          db: Session = Depends(get_db)):
    """Обновляем категорию по её id"""
    stmt = select(CategoryModel).where(CategoryModel.id == category_id,
                                       CategoryModel.is_active)
    
    db_category = db.scalars(stmt).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category.parent_id is not None:
        parent_stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id,
                                                  CategoryModel.is_active)
        parent = db.scalars(parent_stmt).first()
        if parent is None:
            raise HTTPException(status_code=400, detail="Parent category not found")
        

    update_stmt = (update(CategoryModel)
                   .where(CategoryModel.id == category_id)
                   .values(**category.model_dump()))
    
    db.execute(update_stmt)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=200)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Лолгически удаляет категорию по id устанавливая is_active=False"""
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active)
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(is_active=False)) # db.scalars не используется, т.ек. update не возвращает объекты модели, а выполняет изменение в БД
    # category.is_active = False
    db.commit()

    return {"status": "success", "message": "Category marked as inactive"}


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

