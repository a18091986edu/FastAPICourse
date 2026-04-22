from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

# p = Path(title,
#          description,
#          examples,
#          include_in_schema,
#          min_length,
#          max_length,
#          pattern,
#          gt,
#          ge,
#          lt,
#          le
#     )

# q = Query(title,
#          description,
#          examples,
#          include_in_schema,
#          min_length,
#          max_length,
#          pattern,
#          gt,
#          ge,
#          lt,
#          le
#     )


@app.get("/users/{username}")
async def login(
    age: int,
    username: str = Path(
        min_length=3,
        max_length=15,
        description="Enter your username",
        examples=["Ilya"],
    ),
) -> dict:
    return {"user": username, "age": age}


# Annotated позволяет использовать тип и валидацию без присваивания значения по умолчанию, что устраняет проблему порядка - следования обязательных аргументов до аргументов со значением по умолчанию


@app.get("/users/{username}")
async def login1(
    username: Annotated[
        str,
        Path(
            min_length=3, max_length=15, description="Enter username", examples=["Ilya"]
        ),
    ],
    age: int,
):
    return {"user": username, "age": age}


# http://127.0.0.1:8000/user?people=Tom&people=Sam


@app.get("/user")
async def search(
    people: Annotated[
        list[str],
        Query(
            min_length=1,
            max_length=5,
            description="List of user names",
            example=["Tom", "Sam"],
        ),
    ],
) -> dict:
    return {"user": people}


@app.get("/users/{name}")
async def get_user(
    name: Annotated[
        str, Path(min_length=4, max_length=20, description="Enter your name")
    ],
) -> dict:
    return {"user_name": name}


@app.get("/category/{category_id}/products")
async def category(
    category_id: Annotated[int, Path(gt=0, description="Category_id")], page: int
) -> dict:
    return {"category_id": category_id, "page": page}


@app.get("/users")
async def retrieve_user_profile(
    username: Annotated[
        str, Query(min_length=2, max_length=50, description="Имя пользователя")
    ],
) -> dict:
    return (
        profiles_dict[username] #noqa
        if username in profiles_dict #noqa
        else {"message": f"Пользователь {username} не найден."}
    )
