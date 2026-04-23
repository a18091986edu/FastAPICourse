from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from database import get_async_db

from app.models.event import EventModel
from app.schemas.event import EventSchema

router = APIRouter(prefix="/events")

@router.get("/{event_id}", response_model=EventSchema)
async def get_event(event_id: int, db: AsyncSession = Depends(get_async_db)):
    event = await db.scalar(select(
        EventModel
    )
    .where(
        EventModel.id == event_id, EventModel.is_active
    ))

    if not event:
        raise HTTPException(404)
    
    return event























from app.models.category import CategoryModel
from app.schemas.category import CategorySchema, CategoryCreate

router = APIRouter(prefix='/categories')

@router.post('/', response_model=CategorySchema, status_code=201)
async def create_category(
    data: CategoryCreate, db: AsyncSession = Depends(get_async_db)
):
    
    db.add(new_category := CategoryModel(**data.model_dump()))
    await db.commit()
    await db.refresh(new_category)
    return new_category

























from app.models.order import OrderModel
from app.schemas.order import OrderSchema

router = APIRouter(prefix="/orders")

@router.get("/", response_model=list[OrderSchema])
async def get_orders(db: AsyncSession = Depends(get_async_db)):
    return (await db.scalars(
                  select(
                      OrderModel
                  )
                  .where(
                      OrderModel.is_active
                  ))).all()


from app.models.promocode import PromoCodeModel

router = APIRouter(prefix="/promocodes")

@router.delete("/{promocode_id}", response_model=dict)
async def delete_promocode(promocode_id: int, db: AsyncSession = Depends(get_async_db)):
    promocode_db = await db.scalar(
        select(PromoCodeModel).where(
            PromoCodeModel.id == promocode_id, PromoCodeModel.is_active
        )
    )

    if not promocode_db:
        raise HTTPException(404)
    

    promocode_db.is_active = False

    db.commit()

    return {"status": "success", "message": "Promocode marked as inactive"}





























from app.models.subscription import SubscriptionModel
from app.models.user import UserModel

from app.schemas.subscription import SubscriptionSchema, SubscriptionUpdate

router = APIRouter(prefix="/subscriptions")

@router.put("/{subscription_id}", response_model=SubscriptionSchema)
async def change_subscription(subscription_id: int, 
                              data: SubscriptionUpdate,
                              db: AsyncSession = Depends(get_async_db)):
    sub_db = await db.scalar(
        select(
            SubscriptionModel
        )
        .where(
            SubscriptionModel.id == subscription_id,
            SubscriptionModel.is_active
        )
    )

    if not sub_db:
        raise HTTPException(404)
    

    user_db = await db.scalar(
        select(
            UserModel
        )
        .where(
            UserModel.id == sub_db.user_id, UserModel.is_active
        )
    )

    if not user_db:
        raise HTTPException(404)

    await db.execute(
        update(SubscriptionModel)
        .where(SubscriptionModel.id == subscription_id, SubscriptionModel.is_active)
        .values(**data.model_dump(exclude_unset=True))
    )

    await db.commit()
    db.refresh(sub_db)
    return sub_db 









































from app.models.product import ProductModel
from app.models.review import ReviewModel


router = APIRouter(prefix="/reviews")

@router.delete("/{review_id}", response_model=dict)
async def review_delete(review_id: int, db: AsyncSession = Depends(get_async_db)):
    db_review = await db.scalar(
        select(
            ReviewModel
        )
        .where(
            ReviewModel.id == review_id, ReviewModel.is_active
        )
    )
    if not db_review:
        raise HTTPException(404)
    

    db_product = await db.scalar(
        select(
            ProductModel
        )
        .where(
            ProductModel.id ==  db_review.product_id, ProductModel.is_active
        )
    )

    if not db_product:
        raise HTTPException(404)
    
    db_review.is_active = False
    await db.commit()

    return {"status": "success", "message": "Review marked as inactive"}

























from app.models.task import TaskModel
from app.models.project import ProjectModel
from app.schemas.task import TaskUpdate, TaskSchema

router = APIRouter(prefix="/tasks")

@router.put("/{task_id}", response_model=TaskSchema, status_code=201)
async def update_task(task_id: int, 
                      task: TaskUpdate, 
                      db: AsyncSession = Depends(get_async_db)):
    db_task = await db.scalar(select(TaskModel).where(
        TaskModel.id == task_id, TaskModel.is_active
    ))

    if not db_task:
        raise HTTPException(404, detail="Not exists")
    
    project = await db.scalar(select(ProjectModel).where(
        ProjectModel.id == task.project_id, ProjectModel.is_active
    ))

    if not project:
        raise HTTPException(404, detail="Not exists")
    

    await db.execute(
        update(TaskModel)
        .where(TaskModel.id == task_id, TaskModel.is_active).values(
        **task.model_dump(exclude_unset=True))
        )

    await db.commit()
    await db.refresh(db_task)

    return db_task

































from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketSchema
from app.models.user import UserModel


router = APIRouter(prefix="/tickets")

@router.post("/", response_model=TicketSchema, status_code=201)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_async_db)):
    
    user_db = await db.scalar(select(UserModel).where(
        UserModel.id == ticket.user_id, UserModel.is_active
    ))

    if not user_db:
        raise HTTPException(status_code=400)

    db.add(db_ticket := TicketModel(**ticket.model_dump()))
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket




























from app.models.message import MessageModel
from app.schemas.message import MessageSchema

router = APIRouter("/messages")

@router.get("/{message_id}", 
            response_model=MessageSchema,
            status=200)
async def get_message_by_id(message_id: int, 
                            db: AsyncSession = Depends(get_async_db)):
    db_m = await db.scalar(select(
        MessageModel
    ).where(
        MessageModel.is_active, MessageModel.id == message_id
    ))

    if not db_m:
        raise HTTPException(status_code=404, detail="Not found")
    
    return db_m






















from app.models.project import ProjectModel
from app.schemas.project import ProjectSchema


router = APIRouter("/projects")

@router.get("/", 
            response_model=list[ProjectSchema], 
            status_code=200)
async def get_all_projects(
    db: AsyncSession = Depends(get_async_db)):

    return (await db.scalars(
        select(
            ProjectModel
        ).where(
            ProjectModel.is_active
        ))).all()