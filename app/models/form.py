from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    groups = relationship("StudentGroup")
