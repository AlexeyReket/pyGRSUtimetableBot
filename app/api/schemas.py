from typing import List, Optional

from pydantic import BaseModel


class FacultySchema(BaseModel):
    name: str


class CourseSchema(BaseModel):
    num: int


class FormSchema(BaseModel):
    type: str


class GroupSchema(BaseModel):
    name: str = None
    faculty_id: int = None
    course_id: int = None
    form_id: int = None
    status_code: int = None


class TimetableSchema(BaseModel):
    group_id: int
    schedule: str


class UserSchema(BaseModel):
    chat_id: int = None
    username: str = None
    password: str = None
    role_code: int = None
    role_name: str = None
    get_comics: bool = None


class GroupUserSchema(BaseModel):
    user_id: int
    group_id: int


class LoginSchema(BaseModel):
    login: str
    password: str
    rt: str = None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: Optional[str] = None
