from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def get_all_products():
    """Возвращает список всех товаров"""
    return {}


@router.post("/")
async def create_product():
    """Создвает новый товар"""
    return {}


@router.get("/category/{category_id}")
async def get_products_ny_category(category_id: int):
    """Возвращает список товаров в указанной категории по её id"""
    return {}


@router.get("/{product_id}")
async def get_product(product_id: int):
    """Возвращает детальну информацию о товаре"""
    return {}


@router.put("/{product_id}")
async def update_product(product_id: int):
    """Обновляет товар по его ID"""
    return {}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Удаляет товар по его ID"""
    return {}
