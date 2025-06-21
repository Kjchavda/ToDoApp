from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth_router, tags_router, todos_router

from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",       # React dev server
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Allow these origins
    allow_credentials=True,
    allow_methods=["*"],              # ✅ Allow all HTTP methods
    allow_headers=["*"],              # ✅ Allow all headers (including Authorization)
)

app.include_router(todos_router.todos_router)
app.include_router(tags_router.tags_router)
app.include_router(auth_router.auth_router)


@app.get("/")
def root():
    return{"Hello World"}