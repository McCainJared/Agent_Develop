from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Agent!"}

@app.get("/todos")
def get_todos():
    return [
        {"id": 1, "title": "学习 FastAPI", "completed": False},
        {"id": 2, "title": "搭建 API", "completed": True},
    ]