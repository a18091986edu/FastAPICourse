from typing import Annotated
from fastapi import Body, FastAPI, APIRouter, Depends, HTTPException, Path
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from database import get_db

from app.models.post import PostModel

router = APIRouter(prefix="/posts")

@router.delete("/{post_id}", response_model=str)
async def delete_post(post_id: int, 
                      db: Session = Depends(get_db)) -> str:
    post = db.scalars(
        select(PostModel).where(PostModel.is_active,
                                PostModel.id == post_id)
    ).first()

    if not post:
        raise HTTPException(404)
    
    post.is_active = False
    db.commit()
    return "Post marked as inactive"














































# from app.models.review import ReviewModel
# from app.schemas.review import ReviewCreate, ReviewSchema
# from app.models.product import ProductModel

router = APIRouter(prefix="/review")

@router.put("/{review_id}", response_model=ReviewSchema)
async def change_review(
    review_id: Annotated[int, Path(...)],
    review: Annotated[ReviewCreate, Body(...)],
    db: Session = Depends(get_db)):
    review_db = db.scalars(
        select(ReviewModel)
        .where(ReviewModel.id == review_id,
               ReviewModel.is_active)
    ).first()

    if not review_db:
        raise HTTPException(404)
    
    product = db.scalars(
        select(ProductModel).where(
            ProductModel.id == review_db.product_id, ProductModel.is_active
        )
    ).first()

    if not product:
        raise HTTPException(404)
    

    db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == review_id)
        .values(**review.model_dump())
    )
    db.commit()
    db.refresh(review_db)
    return review_db
























from app.models.order import OrderModel
from app.models.user import UserModel
from app.schemas.order import OrderSchema

router = APIRouter(prefix="/orders")


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_by_id(
    order_id: Annotated[int, Path(...)], db: Session = Depends(get_db)
):

    order = db.scalars(
        select(OrderModel).where(order_id == OrderModel.id, OrderModel.is_active)
    ).first()
    if not order:
        raise HTTPException(detail="Order not found", status_code=404)

    user = db.scalars(
        select(UserModel).where(UserModel.id == order.user_id, UserModel.is_active)
    ).first()
    if not user:
        raise HTTPException(detail="User not found", status_code=404)

    return order


# from app.schemas.category import CategorySchema, CategoryCreate
# from app.models.category import CategoryModel

router = APIRouter(prefix="/categories")

@router.post("/", response_model=CategorySchema,
             status_code=201)
async def create_category(category: CategoryCreate,
                          db: Session = Depends(get_db)):
    category = CategoryModel(**category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# from app.models.user import UserModel
# from app.schemas.user import UserSchema

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[UserSchema])
async def get_active_users(db: Session = Depends(get_db)):
    return db.scalars(
        select(UserModel).where(UserModel.is_active)
    ).all()

