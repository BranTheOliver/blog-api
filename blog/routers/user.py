from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database
from ..crud import user

router = APIRouter(prefix="/user", tags=["User"])

get_db = database.get_db


@router.post("/", response_model=schemas.UserResponse)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)