from fastapi import Body, FastAPI, status, Path
from fastapi.exceptions import HTTPException
from typing import Annotated
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, NonNegativeInt, PositiveInt, SecretStr

app = FastAPI()

class Note(BaseModel):
    id: Annotated[PositiveInt, Field(...)]
    text: Annotated[str, Field(...)]


notes = [
    Note(id=1, text="Купить хлеб"),
    Note(id=2, text="Написать отчет"),
    Note(id=3, text="Позвонить маме"),
    Note(id=4, text="Сходить в спортзал"),
    Note(id=5, text="Прочитать книгу")
]


@app.delete("/notes/{note_id}", status_code=200, response_model=Note)
async def delete_note(note_id: Annotated[int, Path()]) -> Note:
    note_index = next((idx for idx, note in enumerate(notes) if note.id == note_id), None)
    if note_index is None:
        raise HTTPException(detail="Note not found", status_code=404)
    return notes.pop(note_index)
    


class IdMixIn(BaseModel):
    id: Annotated[int, Field(...)]

class UserCreate(BaseModel):
    name: Annotated[str, Field(...)]
    age: Annotated[str, Field(...)]
    
class User(UserCreate, IdMixIn):
    pass

class UserUpdate(UserCreate):
    pass

users = [
    User(id=1, name="Алексей", age=25),
    User(id=2, name="Мария", age=30),
    User(id=3, name="Иван", age=22),
    User(id=4, name="Елена", age=28),
    User(id=5, name="Дмитрий", age=35)
]

@app.patch("/users/{user_id}", 
           status_code=status.HTTP_200_OK, 
           response_model=User)
async def update_user(user_id = Annotated[int, Path(...)],
                      user_data = Annotated[UserUpdate, Body(...)]) -> User:
    if user_data.id not in [u.id for u in users]:
        raise HTTPException(detail="User not found", status_code=404)
    del [u for u in users if u.id == user_id][0]
    users.append(updated_user:=User(**user_data, id=user_id))
    return updated_user

users = [
    User(id=1, name="Алексей", email="alexey@example.com"),
    User(id=2, name="Мария", email="maria@example.com"),
    User(id=3, name="Иван", email="ivan@example.com"),
    User(id=4, name="Елена", email="elena@example.com"),
    User(id=5, name="Дмитрий", email="dmitry@example.com")
]

@app.get("/users/{user_id}", status_code=200, response_model=User)
async def get_user(user_id: Annotated[int, Path(...)]) -> User:
    if user_id not in [u.id for u in users]:
        raise HTTPException(detail="User not found", status_code=404)
    return [u for u in users if u.id == user_id][0]

@app.post("/users", status_code=201, response_model=User)
async def create_user(user: UserCreate) -> User:
    users.append(new_user:=User(**user.model_dump(), id=len(users)))
    return new_user








class Task(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    completed: bool = Field(...)

tasks = [
    Task(id=1, title="Купить молоко", completed=False),
    Task(id=2, title="Позвонить другу", completed=True),
    Task(id=3, title="Сделать домашку", completed=False),
    Task(id=4, title="Погулять с собакой", completed=True),
    Task(id=5, title="Записаться на тренировку", completed=False)
]


@app.get("/tasks", response_model=list[Task], status_code=200)
async def get_tasks() -> list[Task]:
    return tasks










class Message(BaseModel):
    id: int
    content: str
    password: SecretStr

message = Message(id=1, content="new message", password="test")

mes_model_dump = message.model_dump()
mes_model_dump_json = message.model_dump_json(indent=2)

print(f"{mes_model_dump=}, {type(mes_model_dump)}")
print(f"{mes_model_dump_json=}, {type(mes_model_dump_json)}")
print(mes_model_dump_json)
print(message.password.get_secret_value())


# Специализированные типы pydantic
# EmailStr, HttpUrl, PositiveInt, NegativeFloat, NonNegativeInt, NegativeFloat, constr, conint, SecretStr


class User(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(description="Электронная почта пользователя")
    is_active: bool = Field(default=True, description="Статус активности пользователя")


class Task(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Название задачи")
    description: str | None = Field(default=None, max_length=500, description="Описание задачи")
    is_completed: bool = Field(default=False, description="Статус завершения задачи")

task = Task(title='test', description='test', is_completed=True)
print(task)
task = Task(title='test', is_completed=True)
print(task)
task = Task(title='test')
print(task)
task = Task(title='test', description='None')
print(task)
task = Task(description='None')
print(task)

class Order(BaseModel):
    order_id: PositiveInt = Field(..., description="Уникальный идентификатор заказа")
    user_id: PositiveInt = Field(..., description="Идентификатор пользователя, сделавшего заказ")
    total_amount: Decimal = Field(..., ge=0, description="Общая сумма заказа")
    created_at: datetime = Field(..., description="Дата и время создания заказа")

class Address(BaseModel):
    user_id: PositiveInt = Field(..., description="Идентификатор пользователя")
    city: str = Field(..., min_length=2, max_length=100, description="Город")
    street: str = Field(..., min_length=2, max_length=200, description="Улица")
    postal_code: int = Field(..., ge=101000, le=999999, description="Почтовый индекс")


class Product(BaseModel):
    product_slug: str = Field(..., min_length=3, 
                              max_length=120, 
                              pattern=r'^[A-Za-z0-9_-]+$',
                              description="Слаг продукта"
                            )
    
    name: str = Field(..., min_length=3, max_length=100, description="Название продукта")
    price: Decimal = Field(..., gt=0, description="Цена продукта")
    stock: NonNegativeInt = Field(default=0, description="Коичество продукта на складе")


class Post(BaseModel):
    author_id: PositiveInt = Field(..., description="Идентификатор автора")
    title: str= Field(..., max_length=100, description="Заголовок записи, не более 100 символов")
    content: str = Field(..., description="Контент записи")
    description: str | None = Field(max_length=250, description="Описание записи, не более 250 символов", default=None)
    created_at: datetime = Field(default_factory=datetime.now, description="Запись создана")
    updated_at: datetime | None = Field(default=None, description="Запись обновлена")
    is_published: bool = Field(default=False, description="Запись опубликована")
    tags: list[str] = Field(default=list(), description="Теги записи")



class User(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, description="Пользовательское имя, от 5 до 20 символов")
    password: SecretStr = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")
    first_name: str | None = Field(min_length=2, max_length=30, default=None, description="Имя, от 2 до 30 символов")
    last_name: str | None = Field(min_length=2, max_length=30, default=None, description="Фамилия, от 2 до 30 символов")
    is_active: bool = Field(default=True, description="Учётная запись активна")
    is_staff: bool = Field(default=False, description="Является служебным пользователем")
    is_superuser: bool = Field(default=False, description="Является суперпользователем")
    date_joined: datetime = Field(default_factory=datetime.now, description="Зарегистрирован")
    last_login: datetime | None = Field(default=None, description="Последнее посещение")


