from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime, timezone

from ..models.note_model import Note
    

class User(BaseModel):
    created_at:Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    first_name: str
    last_name : str
    email:EmailStr
    password:str
    notes: List[Note] = Field(default_factory=list)  # Default to an empty list of Note instances  
    salt:Optional[str] = None  
    
    
