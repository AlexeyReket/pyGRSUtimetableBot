from .static_info import StaticInfo
from .faculty import Faculty
from .course import Course
from .student_group import StudentGroup, GroupUser
from .form import Form
from .user import User

from main import Base

__all__ = [Base, Course, Form, Faculty, StudentGroup, User, GroupUser, StaticInfo]
