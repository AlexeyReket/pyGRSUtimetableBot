import datetime

from sqlalchemy import Column, Date, Integer

from main import Base


class StaticInfo(Base):
    __tablename__ = "static"
    id = Column(Integer, primary_key=True)
    comics_date = Column(Date, nullable=False, default=datetime.date.today())
