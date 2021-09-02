from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from main import Base


class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    groups = relationship("StudentGroup", viewonly=True)
