import uvicorn
from fastapi import Depends, FastAPI

from src import config
from .api.users import user_router

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=config.DEBUG_MODE,
        port=config.PORT
    )