from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class BlogResponse(BaseModel):
    class Config:
        orm_mode = True