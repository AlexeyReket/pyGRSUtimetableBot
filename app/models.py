from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    groups = relationship("StudentGroup")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    groups = relationship("StudentGroup")


class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    groups = relationship("StudentGroup")


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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("StudentGroup", lazy='joined')

