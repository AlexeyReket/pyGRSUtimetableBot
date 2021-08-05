import uvicorn
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
if __name__ == "__main__":
    uvicorn.run(
        "api.control:app",
        host='localhost',
        port=8000,
        reload=True
    )
