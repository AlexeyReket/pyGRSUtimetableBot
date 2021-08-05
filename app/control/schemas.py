from pydantic import BaseModel as Base


class FacultyBody(Base):
    name: str


class CourseBody(Base):
    num: int


class FormBody(Base):
    type: str


class GroupBody(Base):
    name: str = None
    faculty_id: int
    course_id: int
    form_id: int


class UserBody(Base):
    chat_id: int
    group_id: int = None
