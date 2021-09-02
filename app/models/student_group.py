import enum

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from main import Base


class StudentGroup(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", lazy="joined")
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", lazy="joined")
    form_id = Column(Integer, ForeignKey("forms.id"))
    form = relationship("Form", lazy="joined")
    status_code = Column(Integer, nullable=False, default=0)
    status_name = Column(String, nullable=False, default="waiting")
    current_schedule = Column(String)
    last_schedule = Column(String)


class GroupStatus(enum.Enum):
    waiting = 0
    disputed = 1
    completed = 2
    updated = 3
    muted = 4


class GroupUser(Base):
    __tablename__ = "groups_link_users"
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group = relationship("StudentGroup", lazy="joined", cascade="all,delete")
    user = relationship("User", lazy="joined")
