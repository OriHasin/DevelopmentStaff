from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models import Settings, Task
from typing import List, Dict, Any
from datetime import datetime


app = FastAPI()
setting = Settings()

client = AsyncIOMotorClient(setting.mongo_url)
db = client['TasksDB']
collection = db["tasks"]


@app.on_event("startup")
async def create_indexes():
    await collection.create_index([("completed", 1)])
    await collection.create_index([("due_date", 1)])


@app.on_event("shutdown")
async def clean_resources():
    client.close()


@app.get('/get/', response_model=List[Task])
async def get_all_tasks(limit: int = 10, page: int = 1):
    results = collection.find().sort("_id", 1).skip((page - 1) * limit).limit(limit)
    results = await results.to_list()

    if results:
        return results
    raise HTTPException(status_code=404, detail="No tasks found...")


@app.get('/get/{user_id}', response_model=List[Task])
async def get_all_tasks(user_id: int, limit: int = 10, page: int = 1):
    results = collection.find({"user_id": user_id}).sort("_id", 1).skip((page - 1) * limit).limit(limit)
    results = await results.to_list()
    if results:
        return results
    raise HTTPException(status_code=404, detail=f"No tasks found for user {user_id}...")


@app.post("/create/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_task(tasks: Task):
    result = await collection.insert_one(tasks.model_dump(exclude_none=True))

    if result.inserted_id:
        return {"message": "Successfully added tasks!",
                "tasks": tasks.model_dump(exclude_none=True)}
    raise HTTPException(status_code=500, detail="Cannot add tasks, internal error...")


@app.put("/update/{task_title}", status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_title: str, updated_task: Task):
    result = await collection.update_one({"title": task_title}, {"$set": updated_task.model_dump(exclude_none=True)})

    if result.matched_count == 1:
        return {"message": "Successfully updated task!",
                "task": updated_task.model_dump()}
    raise HTTPException(status_code=500, detail="Didn't update, internal error...")


@app.delete("/delete/{task_title}", status_code=status.HTTP_202_ACCEPTED)
async def delete_task(task_title: str):
    result = await collection.delete_one({"title": task_title})

    if result.deleted_count == 1:
        return {"message": "Successfully deleted task!",
                "title": task_title}
    raise HTTPException(status_code=500, detail="Didn't delete, ")



@app.get("/get/completed/{user_id}", response_model=List[Task])
async def get_completed_tasks(user_id: int, page: int = 1, limit: int = 10):
    result = collection.find({"user_id": user_id, "completed": True}).sort("_id", 1).skip((page-1) * limit).limit(limit)
    result = await result.to_list()
    if result:
        return result
    raise HTTPException(status_code=404, detail="no completed tasks found")



@app.get("/get/tasks/dates/{user_id}", response_model=List[Task])
async def get_completed_tasks(user_id: int, date_range: dict, page: int = 1, limit: int = 10):
    result = collection.find({"user_id": user_id, "due_date": {"$gte": datetime.fromisoformat(date_range['start']), "$lte": datetime.fromisoformat(date_range['end'])}}).sort("_id", 1).skip((page-1) * limit).limit(limit)
    result = await result.to_list()
    if result:
        return result
    raise HTTPException(status_code=404, detail="no dated tasks found")
