from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    groups = relationship("StudentGroup")
