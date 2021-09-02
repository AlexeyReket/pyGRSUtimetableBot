import datetime

from sqlalchemy.orm import sessionmaker
from models.static_info import StaticInfo

from main import engine

Session = sessionmaker(bind=engine)
session = Session()


def check_last_date() -> StaticInfo:
    info = session.query(StaticInfo).filter_by(id=1).one()
    session.close()
    return info


def put_date(comics_date: datetime.date) -> str:
    info = session.query(StaticInfo).filter_by(id=1)
    info.update({"comics_date": comics_date})
    session.commit()
    session.close()
    return "success"
