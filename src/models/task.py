from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in-progress, completed
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    user_id: str  # ID del usuario propietario