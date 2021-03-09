from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"api": "fastapi"}}


@app.get("/about")
def about():
    return {"data": ["about page"]}