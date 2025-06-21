from fastapi import FastAPI

from app.routers import auth_router, tags_router, todos_router

from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos_router.todos_router)
app.include_router(tags_router.tags_router)
app.include_router(auth_router.auth_router)


@app.get("/")
def root():
    return{"Hello World"}