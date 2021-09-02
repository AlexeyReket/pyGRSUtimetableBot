from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from main import Base


class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    groups = relationship("StudentGroup", viewonly=True)
