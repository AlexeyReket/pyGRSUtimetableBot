from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models.course import Course

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_courses(mark: str = "id"):
    courses = session.query(Course).order_by(mark).all()
    session.close()
    return courses


def get_one_course(id: int):
    course = session.query(Course).filter_by(id=id).first()
    session.close()
    return course


def post_course(num: int):
    course_to_add = Course(num=num)
    session.add(course_to_add)
    session.commit()
    session.close()
    return "success"


def put_course(id: int, num: int):
    session.query(Course).filter_by(id=id).update(num=num)
    session.commit()
    session.close()
    return "success"


def delete_all_courses():
    session.query(Course).delete()
    session.commit()
    session.close()
    return "success"


def delete_course(id: int):
    session.query(Course).filter_by(id=id).delete()
    session.commit()
    session.close()
    return "success"
