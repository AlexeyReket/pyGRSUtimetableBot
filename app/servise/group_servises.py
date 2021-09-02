from typing import List

from sqlalchemy.orm import sessionmaker
from models.student_group import StudentGroup, GroupStatus, GroupUser

from main import engine

Session = sessionmaker(bind=engine)
session = Session()


def get_groups(group_id: int = None, name: str = None, faculty_id: int = None, course_id: int = None,
               form_id: int = None, status_code: int = None, mark: str = "id") -> List[StudentGroup]:
    query = session.query(StudentGroup)
    if group_id:
        query = query.filter_by(id=group_id)
    if name:
        query = query.filter_by(name=name)
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    if course_id:
        query = query.filter_by(course_id=course_id)
    if form_id:
        query = query.filter_by(form_id=form_id)
    if status_code:
        query = query.filter_by(status_code=status_code)
    groups = query.order_by(mark).all()
    session.close()
    return groups


def get_group(group_id: int) -> StudentGroup:
    group = session.query(StudentGroup).filter_by(id=group_id).first()
    session.close()
    return group


def post_group(name: str, faculty_id: int, course_id: int, form_id: int, status: int) -> str:
    group_to_add = StudentGroup(name=name, faculty_id=faculty_id, course_id=course_id, form_id=form_id,
                                status_code=status, status_name=GroupStatus(status).name)
    session.add(group_to_add)
    session.commit()
    session.close()
    return "success"


def post_group_user(user_id: int, group_id: int) -> str:
    group_user_to_add = GroupUser(user_id=user_id, group_id=group_id)
    session.add(group_user_to_add)
    session.commit()
    session.close()
    return "success"


def put_group(group_id: int, name: str = None, faculty_id: int = None, course_id: int = None, form_id: int = None,
              status_code: int = None, current_schedule: str = None) -> str:
    group = session.query(StudentGroup).filter_by(id=group_id)
    if name:
        group.update({"name": name})
    if faculty_id:
        group.update({"faculty_id": faculty_id})
    if course_id:
        group.update({"course_id": course_id})
    if form_id:
        group.update({"form_id": form_id})
    if status_code:
        group.update({"status_code": status_code, "status_name": GroupStatus(status_code).name})
    if current_schedule:
        group.update({"last_schedule": group.one().current_schedule, "current_schedule": current_schedule})
    session.commit()
    session.close()
    return "success"


def get_all_link(group_id: int = None, user_id: int = None) -> List[GroupUser]:
    links = session.query(GroupUser)
    if group_id:
        links = links.filter_by(group_id=group_id)
    if user_id:
        links = links.filter_by(user_id=user_id)
    links = links.all()
    session.close()
    return links


def approve_all_waiting_groups() -> str:
    groups = session.query(StudentGroup).filter_by(status_code=GroupStatus.waiting.value)
    groups.update({"status_code": GroupStatus.completed.value, "status_name": GroupStatus.completed.name})
    session.commit()
    session.close()
    return "success"


def delete_all_groups() -> str:
    session.query(StudentGroup).delete()
    session.commit()
    session.close()
    return "success"


def delete_group(group_id: int) -> str:
    group = session.query(StudentGroup).filter_by(id=group_id)
    group.delete()
    session.commit()
    session.close()
    return "success"


def delete_group_user(user_id: int, group_id: int) -> str:
    group_user = session.query(GroupUser).filter_by(user_id=user_id, group_id=group_id)
    group_user.delete()
    session.commit()
    session.close()
    return "success"
