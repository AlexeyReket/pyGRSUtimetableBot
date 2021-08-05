from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class StudentGroup(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", lazy='joined')
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", lazy='joined')
    form_id = Column(Integer, ForeignKey("forms.id"))
    form = relationship("Form", lazy='joined')
    users = relationship("User", lazy='joined')
