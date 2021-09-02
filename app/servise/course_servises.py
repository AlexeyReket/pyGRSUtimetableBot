from typing import List

from sqlalchemy.orm import sessionmaker
from models.course import Course

from main import engine

Session = sessionmaker(bind=engine)
session = Session()


def get_courses(mark: str = "id") -> List[Course]:
    courses = session.query(Course).order_by(mark).all()
    session.close()
    return courses


def get_course(course_id: int) -> Course:
    course = session.query(Course).filter_by(id=course_id).first()
    session.close()
    return course


def post_course(num: int) -> str:
    course_to_add = Course(num=num)
    session.add(course_to_add)
    session.commit()
    session.close()
    return "success"


def put_course(course_id: int, num: int) -> str:
    session.query(Course).filter_by(id=course_id).update({"num": num})
    session.commit()
    session.close()
    return "success"


def delete_all_courses() -> str:
    session.query(Course).delete()
    session.commit()
    session.close()
    return "success"


def delete_course(course_id: int) -> str:
    session.query(Course).filter_by(id=course_id).delete()
    session.commit()
    session.close()
    return "success"
