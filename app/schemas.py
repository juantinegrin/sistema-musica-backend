from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class ScheduleBase(BaseModel):
    teacher_id: UUID
    room_id: UUID
    start_time: datetime
    end_time: datetime
    is_replacement: bool = False
    notes: Optional[str] = None
    enrollment_id: Optional[UUID] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: UUID
    class Config:
        from_attributes = True