from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional
from datetime import datetime



class Settings(BaseSettings):
    mongo_url: str
    class Config:
        env_file = ".env"


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False # maybe need field
    due_date: Optional[datetime]
    user_id: int

