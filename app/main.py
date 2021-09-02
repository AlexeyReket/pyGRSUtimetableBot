import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from app import settings

Base = declarative_base()
engine = create_engine(settings.SQLALCHEMY_URL)
app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(
        "api.control:app",
        host='localhost',
        port=8000,
        reload=True
    )
