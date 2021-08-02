from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from validationBodys import *
from models import *
import uvicorn

app = FastAPI()
Session = sessionmaker()
engine = create_engine("sqlite:///data.db", echo=True)
Session.configure(bind=engine)
session = Session()
"""get all requests"""


@app.get("/faculties/all")
def faculty():
    return session.query(Faculty).all()


@app.get("/courses/all")
def course():
    return session.query(Course).all()


@app.get("/forms/all")
def form():
    return session.query(Form).all()


@app.get("/groups/all")
def group():
    return session.query(StudentGroup).all()


"""get one requests"""


@app.get("/faculties/{id}")
def faculty(id):
    return session.query(Faculty).filter_by(id=id).first()



@app.get("/courses/{id}")
def course(id):
    return session.query(Course).filter_by(id=id).first()


@app.get("/forms/{id}")
def form(id):
    return session.query(Form).filter_by(id=id).first()


@app.get("/groups/{id}")
def group(id):
    curGroup = session.query(StudentGroup).filter_by(id=id).first()
    return curGroup


"""post requests"""


@app.post("/faculties")
def faculty(body: FacultyBody):
    faculty_to_add = Faculty(name=body.name)
    session.add(faculty_to_add)
    return {"result": "success"}


@app.post("/courses")
def course(body: CourseBody):
    course_to_add = Course(num=body.num)
    session.add(course_to_add)
    return {"result": "success"}


@app.post("/forms")
def form(body: FormBody):
    form_to_add = Form(type=body.type)
    session.add(form_to_add)
    return {"result": "success"}


@app.post("/groups")
def group(body: GroupBody):
    group_to_add = StudentGroup(name=body.name, faculty_id=body.faculty_id, course_id=body.course_id,
                                form_id=body.form_id)
    session.add(group_to_add)
    return {"result": "success"}


"""put requests"""


@app.put("/faculties/{id}")
def faculty(id, body: FacultyBody):
    session.query(Faculty).filter(Faculty.id == id).update({"name": body.name})
    session.commit()
    return {"result": "success"}


@app.put("/courses/{id}")
def course(id, body: CourseBody):
    session.query(Course).filter(Course.id == id).update({"num": body.num})
    session.commit()
    return {"result": "success"}


@app.put("/forms/{id}")
def form(id, body: FormBody):
    session.query(Form).filter(Form.id == id).update({"type": body.type})
    session.commit()
    return {"result": "success"}


@app.put("/groups/{id}")
def group(id, body: GroupBody):
    session.query(StudentGroup).filter(StudentGroup.id == id). \
        update({"name": body.name, "faculty_id": body.faculty_id, "course_id": body.course_id, "form_id": body.form_id})
    session.commit()
    return {"result": "success"}


"""delete all requests"""


@app.delete("/faculties/all")
def faculty():
    session.query(Faculty).delete()
    return {"result": "success"}


@app.delete("/courses/all")
def course():
    session.query(Course).delete()
    return {"result": "success"}


@app.delete("/forms/all")
def form():
    session.query(Form).delete()
    return {"result": "success"}


@app.delete("/groups/all")
def group():
    session.query(StudentGroup).delete()
    return {"result": "success"}


"""delete one requests"""


@app.delete("/faculties/{id}")
def faculty(id):
    session.query(Faculty).filter_by(id=id).delete()
    return {"result": "success"}


@app.delete("/courses/{id}")
def course(id):
    session.query(Course).filter_by(id=id).delete()
    return {"result": "success"}


@app.delete("/forms/{id}")
def form(id):
    session.query(Form).filter_by(id=id).delete()
    return {"result": "success"}


@app.delete("/groups/{id}")
def group(id):
    session.query(StudentGroup).filter_by(id=id).delete()
    return {"result": "success"}


if __name__ == "__main__":
    uvicorn.run(
        "control:app",
        host='localhost',
        port=8000,
        reload=True
    )
