from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models.form import Form

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_forms(mark: str = "id"):
    forms = session.query(Form).order_by(mark).all()
    session.close()
    return forms


def get_one_form(id: int):
    form = session.query(Form).filter_by(id=id).all()
    session.close()
    return form


def post_form(type: str):
    form_to_add = Form(type=type)
    session.add(form_to_add).commit().close()
    session.close()
    return "success"


def put_form(id: int, type: str):
    session.query(Form).filter_by(id=id).update(type=type)
    session.commit()
    session.close()
    return "success"


def delete_all_forms():
    session.query(Form).delete()
    session.commit()
    session.close()
    return "success"


def delete_form(id: int):
    session.query(Form).filter_by(id=id).delete()
    session.commit()
    session.close()
    return "success"
