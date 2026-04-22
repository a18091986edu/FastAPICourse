from fastapi import APIRouter

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
async def get_all_categories():
    """Возвращаем список всех категорий товаров"""
    return {"message": "Список всех категорий"}


@router.post("/")
async def create_category():
    """Создёт новую категорию"""
    return {}


@router.put("/{category_id}")
async def update_category(category_id: int):
    return {}


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    return {}
