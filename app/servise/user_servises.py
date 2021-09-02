from typing import List

from sqlalchemy.orm import sessionmaker

from main import engine
from models import User
from models.user import UserRole
from servise import auth

Session = sessionmaker(bind=engine)
session = Session()


def get_user(user_id: int = None, chat_id: int = None, name: str = None) -> User:
    user = session.query(User)
    if chat_id:
        user = user.filter_by(chat_id=chat_id)
    elif name:
        user = user.filter_by(name=name)
    elif user_id:
        user = user.filter_by(id=user_id)
    user = user.one()
    session.close()
    return user


def get_users(get_comics: bool = None) -> List[User]:
    users = session.query(User)
    if type(get_comics) == bool:
        users = users.filter_by(get_comics=get_comics)
    users = users.all()
    session.close()
    return users


def post_user(chat_id: int = None, username: str = None, password: str = None) -> str:
    user_to_add = User(chat_id=chat_id, role_code=UserRole.guest.value, username=username,
                       hashed_password=auth.get_password_hash(password), role_name=UserRole.guest.name)
    session.add(user_to_add)
    session.commit()
    session.close()
    return "success"


def put_user(chat_id: int, role_code: int = None, hashed_password: str = None, username: str = None,
             get_comics: bool = None) -> str:
    user = session.query(User).filter_by(chat_id=chat_id)
    if role_code:
        user.update({"role_code": role_code, "role_name": UserRole(role_code).name})
    if hashed_password:
        user.update({"hashed_password": hashed_password})
    if username:
        user.update({"username": username})
    if type(get_comics) == bool:
        user.update({"get_comics": get_comics})
    session.commit()
    session.close()
    return "success"


def delete_user_by_id(user_id) -> str:
    session.query(User).filter_by(id=user_id).delete()
    session.commit()
    session.close()
    return "success"
