from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str  # In a real app, you might use EmailStr from pydantic

    hashed_password: str  # Renamed for clarity
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    is_active: bool = True