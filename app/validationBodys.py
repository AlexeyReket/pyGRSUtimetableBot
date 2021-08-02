from pydantic import BaseModel


class FacultyBody(BaseModel):
    name: str


class CourseBody(BaseModel):
    num: int


class FormBody(BaseModel):
    type: str


class GroupBody(BaseModel):
    name: str
    faculty_id: int
    course_id: int
    form_id: int
