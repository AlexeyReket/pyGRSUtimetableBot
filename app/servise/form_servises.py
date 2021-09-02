from typing import List

from sqlalchemy.orm import sessionmaker
from models.form import Form

from main import engine

Session = sessionmaker(bind=engine)
session = Session()


def get_all_forms(mark: str = "id") -> List[Form]:
    forms = session.query(Form).order_by(mark).all()
    session.close()
    return forms


def get_one_form(form_id: int) -> Form:
    form = session.query(Form).filter_by(id=form_id).all()
    session.close()
    return form


def post_form(form_type: str) -> str:
    form_to_add = Form(type=form_type)
    session.add(form_to_add)
    session.commit()
    session.close()
    return "success"


def put_form(form_id: int, form_type: str) -> str:
    session.query(Form).filter_by(id=form_id).update({"type": form_type})
    session.commit()
    session.close()
    return "success"


def delete_all_forms() -> str:
    session.query(Form).delete()
    session.commit()
    session.close()
    return "success"


def delete_form(form_id: int) -> str:
    session.query(Form).filter_by(id=form_id).delete()
    session.commit()
    session.close()
    return "success"
