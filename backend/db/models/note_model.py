from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)


class Note(BaseModel):
    id:Optional[UUID] = Field(default_factory= lambda:uuid4())
#    created_at:Optional[datetime] = Field(default_factory=lambda: utc_now())
    created_at:Optional[datetime] = Field(default_factory= lambda:utc_now())

    updated_at:Optional[datetime] = None
    title:str
    content:str
    
      # Convert UUID to a string when exporting to a dictionary
    def dict(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d["id"] = str(d["id"])  # Convert UUID to a string
        return d

class Note_update_data(BaseModel):
    updated_at:Optional[datetime] = Field(default_factory= lambda: utc_now())
    title: Optional[str] = None
    content: Optional[str] = None
    