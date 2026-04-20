from fastapi import FastAPI, status, Path, HTTPException, Body
from typing import Annotated


app = FastAPI()

notes_db = {0: "Study FastAPI", 1: "I like FastAPI"}
tasks_db = {0: "Study FastAPI", 1: "I like FastAPI"}
reminders_db = {}
quotes_db = {0: "FastAPI lets you build APIs fast with type hints",
              1: "Auto docs at /docs and /redoc with OpenAPI",
              2: "Pydantic validates your data",
              3: "Depends gives clean Dependency Injection",
              4: "Use async def and await for concurrency"}

goals_db = {0: "Learn FastAPI basics",
            1: "Build CRUD app",
            2: "Write tests with TestClient",
            3: "Add authentication",
            4: "Deploy to production"}

comments_db = {0: "First comment in FastAPI"}

@app.get("/notes", status_code=status.HTTP_200_OK)
async def get_notes() -> dict:
    return notes_db


@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: Annotated[int, Path()]) -> dict:
    try:
        return notes_db['task_id']
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: Annotated[int, Path()]):
    try:
        return tasks_db[task_id]
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    

@app.post("/reminders", status_code=status.HTTP_201_CREATED)
async def create_reminder(reminder: Annotated[str, Body(...)]):
    reminders_db[len(reminders_db)] = reminder
    return "Reminder created!"


@app.put("/quotes/{quote_id}")
async def update_quote(
    quote_id: Annotated[int, Path()],
    quote: Annotated[str, Body(...)]
) -> str:
    if quote_id in quotes_db:
        quotes_db[quote_id] = quote
        return "Quote updated!"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    
@app.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: int
) -> str:
    if goals_db.get(goal_id):
        goals_db.pop(goal_id)
        return "Goal deleted!"
    else:
        raise HTTPException(detail="Goal not found", status_code=404)
    

async def check_comment(comment_id: int):
    return comment_id in comments_db



@app.get("/comments", status_code=status.HTTP_200_OK)
async def get_all_comments() -> dict:
    return comments_db

@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def get_comment(comment_id: Annotated[int, Path()]) -> str:
    if await check_comment(comment_id):
        return comments_db[comment_id]
    else:
        raise HTTPException(detail="Comment not found", status_code=404)
    
@app.post("/comments", status_code=201)
async def create_comment(comment: Annotated[str, Body(...)]) -> str:
    comments_db[len(comments_db)] = comment
    return "Comment created!"

@app.put("/comments/{comment_id}", status_code=200)
async def update_comment(comment_id: Annotated[int, Path],
                         comment: Annotated[str, Body(...)]) -> str:
    if await check_comment(comment_id):
        comments_db[comment_id] = comment
        return "Comment updated!"
    else:
        raise HTTPException(detail="Comment not found", status_code=404)
    
@app.delete("/comments/{comment_id}", status_code=200)
async def delete_comment(comment_id: Annotated[int, Path()]) -> str:
    if await check_comment(comment_id):
        comments_db.pop(comment_id)
        return "Comment deleted!"
    else:
        raise HTTPException(detail="Comment not found", status_code=404)
