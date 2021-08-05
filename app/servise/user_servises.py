from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import User

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_users(mark: str = "id"):
    users = session.query(User).order_by(mark).all()
    session.close()
    return users


def get_user_by_chat(chat_id: int = None):
    users = session.query(User).filter_by(chat_id=chat_id).all()
    session.close()
    return users


def get_one_user(id: int):
    user = session.query(User).filter_by(id=id).first()
    session.close()
    return user


def post_user(group_id: int, chat_id: int):
    user_to_add = User(group_id=group_id, chat_id=chat_id)
    session.add(user_to_add)
    session.commit()
    session.close()
    return "success"


def put_user(id: int, chat_id: int, group_id: int):
    session.query(User).filter_by(id=id).update(chat_id=chat_id, group_id=group_id)
    session.commit()
    session.close()
    return "success"


def delete_all_users():
    session.query(User).delete()
    session.commit()
    session.close()
    return "success"


def delete_user(id: int):
    session.query(User).filter_by(id=id).delete()
    session.commit()
    session.close()
    return "success"


def delete_user_sorted(chat_id: int, group_id: int):
    session.query(User).filter_by(chat_id=chat_id, group_id=group_id).delete()
    session.commit()
    session.close()
    return "success"
