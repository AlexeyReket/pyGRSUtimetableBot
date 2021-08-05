from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.faculty import Faculty

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_faculties(mark: str = "id"):
    faculties = session.query(Faculty).order_by(mark).all()
    session.close()
    return faculties


def get_one_faculty(id: int):
    faculty = session.query(Faculty).filter_by(id=id).first()
    session.close()
    return faculty


def post_faculty(name: str):
    faculty_to_add = Faculty(name=name)
    session.add(faculty_to_add)
    session.commit()
    session.close()
    return "success"


def put_faculty(id: int, name: str):
    session.query(Faculty).filter_by(id=id).update(name=name)
    session.commit()
    session.close()
    return "success"


def delete_all_faculties():
    session.query(Faculty).delete()
    session.commit()
    session.close()
    return "success"


def delete_faculty(id: int):
    session.query(Faculty).filter_by(id=id).delete()
    session.commit()
    session.close()
    return "success"
