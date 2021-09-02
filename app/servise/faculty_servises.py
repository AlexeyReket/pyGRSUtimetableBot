from typing import List

from sqlalchemy.orm import sessionmaker
from models.faculty import Faculty

from main import engine

Session = sessionmaker(bind=engine)
session = Session()


def get_all_faculties(mark: str = "id") -> List[Faculty]:
    faculties = session.query(Faculty).order_by(mark).all()
    session.close()
    return faculties


def get_one_faculty(faculty_id: int) -> Faculty:
    faculty = session.query(Faculty).filter_by(id=faculty_id).first()
    session.close()
    return faculty


def post_faculty(name: str) -> str:
    faculty_to_add = Faculty(name=name)
    session.add(faculty_to_add)
    session.commit()
    session.close()
    return "success"


def post_list_of_faculties(names: list) -> str:
    for name in names:
        faculty_to_add = Faculty(name=name)
        session.add(faculty_to_add)
    session.commit()
    session.close()
    return "success"


def put_faculty(faculty_id: int, name: str) -> str:
    session.query(Faculty).filter_by(id=faculty_id).update({"name": name})
    session.commit()
    session.close()
    return "success"


def delete_all_faculties() -> str:
    session.query(Faculty).delete()
    session.commit()
    session.close()
    return "success"


def delete_faculty(faculty_id: int) -> str:
    session.query(Faculty).filter_by(id=faculty_id).delete()
    session.commit()
    session.close()
    return "success"
