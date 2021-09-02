import enum

from sqlalchemy import Integer, Column, String, Boolean

from main import Base


class UserRole(enum.Enum):
    guest = 1
    moderator = 2
    admin = 99


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    username = Column(String)
    hashed_password = Column(String)
    role_code = Column(Integer, nullable=False, default=1)
    role_name = Column(String, nullable=False, default="guest")
    get_comics = Column(Boolean)
