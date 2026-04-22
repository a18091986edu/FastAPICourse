from fastapi import FastAPI
from src.routers import categories, products

app = FastAPI(title="FastAPI интернет магазин", version="0.1.0")

app.include_router(categories.router)
app.include_router(products.router)



@app.get("/")
async def root():
    """Корневой маршурт, подтверждающий, что API работает"""
    return {}
