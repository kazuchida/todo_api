from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import todos
from .database import engine
from .models import todo

# Create database tables
todo.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="TODO API",
    description="API for managing todo items",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the TODO API! Go to /docs for the API documentation."}