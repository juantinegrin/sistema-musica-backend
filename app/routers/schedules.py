from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from app.database import get_db
from app.models import Schedule
from app.schemas import ScheduleCreate, ScheduleResponse

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.get("/", response_model=List[ScheduleResponse])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()

@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    # Validação de choque de horários (Professor ou Sala ocupados)
    conflict = db.query(Schedule).filter(
        and_(
            Schedule.start_time < data.end_time,
            Schedule.end_time > data.start_time,
            or_(
                Schedule.teacher_id == data.teacher_id,
                Schedule.room_id == data.room_id
            )
        )
    ).first()

    if conflict:
        if conflict.teacher_id == data.teacher_id:
            raise HTTPException(status_code=409, detail="Professor indisponível neste horário.")
        if conflict.room_id == data.room_id:
            raise HTTPException(status_code=409, detail="Sala ocupada neste horário.")

    new_schedule = Schedule(**data.model_dump())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule