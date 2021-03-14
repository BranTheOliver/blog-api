from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database
from ..crud import blog

router = APIRouter(prefix="/blog", tags=["Blog"])

get_db = database.get_db


@router.get("/", response_model=List[schemas.BlogResponse])
def get_all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BlogResponse
)
def get_one(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.get_one(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return blog.delete(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)