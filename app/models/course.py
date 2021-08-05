from sqlalchemy import Integer, Column
from sqlalchemy.orm import relationship
from main import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    groups = relationship("StudentGroup")
