from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import schemas
from . import models
from .hashing import Hash
from .database import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.BlogResponse], tags=["blog"])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BlogResponse,
    tags=["blog"],
)
def get_one(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id {id} is not available."}
        # this can be replaced by:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available.",
        )
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available.",
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found.",
        )

    blog.update(request)
    db.commit()
    return "Updated"


@app.post("/user", response_model=schemas.UserResponse, tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash().hash(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schemas.UserResponse, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found.",
        )

    return user
