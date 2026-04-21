# Depends используетяс для внедрения зависимостей в FastAPI и позволяет добавлять зависимости к API методам. Это означает, что выполнение метода зависит от выполнения другой функции или условия


# Формально, зависимость это обычная функци (или класс с методом __call__), которую FastAPI автоматически вызывает перед выполнением эндпоинта. Результат её работы FastAPI передает в обработчик маршрута как аргумент


from typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException, status
from pydantic import BaseModel, NonNegativeInt, Field
from fastapi.requests import Request



app = FastAPI()


####################################################################
# class Post(BaseModel):
#     id: Annotated[NonNegativeInt, Field(...)]
#     text: Annotated[str, Field()]

# db = []

# async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
#     return [{'limit': limit, 'page': page}]

# @app.get("/messages")
# async def all_messages(pagination: list = Depends(pagination_func)):
#     return {"messages": pagination}


# @app.get("/comments")
# async def all_comments(pagination: list = Depends(pagination_func)):
#     return {"comments": pagination}

####################################################################


# async def get_post_or_404(id: int):
#     try:
#         return db[id]
#     except IndexError:
#         raise HTTPException(status_code=404, detail='Index not found')
    
# @app.get("/message/{id}")
# async def get_message(post: Post = Depends(get_post_or_404)):
#     return post

# @app.post("/message", status_code=status.HTTP_201_CREATED)
# async def create_message(post: Post) -> str:
#     post.id = len(db)
#     db.append(post)
#     return f"Message created!"

# @app.put("/message/{id}")
# async def update_message(post: Post = Depends(get_post_or_404)):
#     pass


# @app.delete("/message/{id}")
# async def delete_message(post: Post = Depends(get_post_or_404)):
#     pass

####################################################################

# class PaginatorA:
#     def __init__(self, limit: int = 10, page: int = 1):
#         self.limit = limit
#         self.page = page


# class Paginator:
#     def __init__(self):
#         self.limit = 10
#         self.page = 1

#     def __call__(self, limit: int):
#         if limit < self.limit:
#             return [{'limit': self.limit, 'page': self.page}]
#         else:
#             return [{'page': self.page, 'limit': limit}]

# paginator = Paginator()
# print(paginator(100))

# @app.get("/users")
# async def all_users(pagination: PaginatorA = Depends(PaginatorA)):
#     return {"user": pagination}


# @app.get("/users1")
# async def all_users(pagination: list = Depends(paginator)):
#     return {"user": pagination}


####################################################################

async def sub_dep(request: Request) -> dict:
    exclude = {'_receive', 'send', 'scope', 'stream_consumed'}
    return {k: v for k, v in vars(request).items() if k not in exclude}

async def main_dep(sub_dep_val: dict = Depends(sub_dep)) -> dict:
    return sub_dep_val

@app.get('/test')
async def test_endpoint(test: dict = Depends(main_dep)):
    return test

####################################################################
async def get_limit(limit: Annotated[int, Query(...)] = 10) -> dict:
    return {"limit": limit}


@app.get("/items")
async def items(limit: Annotated[dict, Depends(get_limit)]):
    return limit

####################################################################

async def check_auth(token: Annotated[str, Query(...)]) -> bool:
    if token != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/profile")
async def profile(check_auth: Annotated[bool, check_auth]) -> str:
    return "User is authorized"

####################################################################


async def pagination_path_func(page: int):
    if page < 0:
        raise HTTPException(status_code=404, detail="Page does not exist")
    if page == 0:
        raise HTTPException(status_code=400, detail="Invalid page value")


async def pagination_func(limit: int = Query(10, gt=0), page: int = 1):
    return {'limit': limit, 'page': page}


@app.get("/messages", dependencies=[Depends(pagination_path_func)])
async def all_messages(pagination: dict = Depends(pagination_func)):
    return {"messages": pagination}


####################################################################

log_user = []


def log_client(request: Request):
    log_user.append(request.headers)


app = FastAPI(dependencies=[Depends(log_client)])


@app.get("/log_user")
async def print_log_user():
    return {"user": log_user}