from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog list"}


@app.get("/blog")
def blog(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}

    return {"data": f"{limit} blogs"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "unpublished blogs"}


@app.get("/blog/{id}")
def posts(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int, limit=10):
    return {"data": {id: [1, 2]}}


class Blog(BaseModel):
    id_blog: int
    title: str
    body: str
    published: bool


@app.post("/blog")
def create_blog(blog: Blog):
    return blog
    return {"blog is created"}