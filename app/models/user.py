from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("StudentGroup", lazy='joined')
