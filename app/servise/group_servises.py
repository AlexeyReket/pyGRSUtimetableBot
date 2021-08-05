from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models.student_group import StudentGroup

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_groups(mark: str = "id"):
    groups = session.query(StudentGroup).order_by(mark).all()
    session.close()
    return groups


def get_sorted_groups(faculty_id: int = None, course_id: int = None, form_id: int = None):
    query = session.query(StudentGroup).filter_by(faculty_id=faculty_id)
    if course_id:
        groups = query.filter(course_id=course_id)
    if form_id:
        groups = query.filter(course_id=course_id)

    session.close()
    return groups


def get_one_group(id: int):
    group = session.query(StudentGroup).filter_by(id=id).first()
    session.close()
    return group


def post_group(name: str, faculty_id: int, course_id: int, form_id: int):
    group_to_add = StudentGroup(name=name, faculty_id=faculty_id, course_id=course_id, form_id=form_id)
    session.add(group_to_add)
    session.commit()
    session.close()
    return "success"


def put_group(id: int, name: str, faculty_id: int, course_id: int, form_id: int):
    session.query(StudentGroup).filter_by(id=id).update(name=name, faculty_id=faculty_id, course_id=course_id,
                                                        form_id=form_id)
    session.commit()
    session.close()
    return "success"


def delete_all_groups():
    session.query(StudentGroup).delete()
    session.commit()
    session.close()
    return "success"


def delete_group(id: int):
    session.query(StudentGroup).filter_by(id=id).delete()
    session.commit()
    session.close()
    return "success"
