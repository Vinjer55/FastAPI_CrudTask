import uvicorn
from fastapi import Depends, FastAPI

from src import config
from .api.students import student_router
from .api.auth import auth_router

app = FastAPI()

app.include_router(student_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=config.DEBUG_MODE,
        port=config.PORT
    )