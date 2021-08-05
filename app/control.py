from fastapi import FastAPI
from validationBodys import *
import uvicorn
from servise import user_servises, course_servises, form_servises, group_servises, faculty_servises

app = FastAPI()


"""get all requests"""


@app.get("/faculties/all")
async def faculty():
    return faculty_servises.get_all_faculties()


@app.get("/courses/all")
async def course():
    return course_servises.get_all_courses()


@app.get("/forms/all")
async def form():
    return form_servises.get_all_forms()


@app.get("/users/all")
async def user():
    return user_servises.get_all_users()


@app.get("/groups/all")
async def group():
    return group_servises.get_all_groups("name")


@app.get("/groups/sorted")
async def group(body: GroupBody):
    return group_servises.get_sorted_groups(body.faculty_id, body.course_id, body.form_id)


@app.get("/users/by_tele/{chat_id}")
async def user(chat_id: int):
    return user_servises.get_user_by_chat(chat_id)


"""get one requests"""


@app.get("/faculties/{id}")
def faculty(id: int):
    return faculty_servises.get_one_faculty(id)


@app.get("/courses/{id}")
def course(id: int):
    return course_servises.get_one_course(id)


@app.get("/forms/{id}")
def form(id: int):
    return form_servises.get_one_form(id)


@app.get("/groups/{id}")
def group(id: int):
    return group_servises.get_one_group(id)


@app.get("/users/{id}")
def user(id: int):
    return user_servises.get_one_user(id)


"""post requests"""


@app.post("/faculties")
def faculty(body: FacultyBody):
    result = faculty_servises.post_faculty(body.name)
    return {"result": result}


@app.post("/courses")
def course(body: CourseBody):
    result = course_servises.post_course(body.num)
    return {"result": result}


@app.post("/forms")
def form(body: FormBody):
    result = form_servises.post_form(body.type)
    return {"result": result}


@app.post("/groups")
def group(body: GroupBody):
    result = group_servises.post_group(body.name, body.faculty_id, body.course_id, body.form_id)
    return {"result": result}


@app.post("/users")
def user(body: UserBody):
    result = user_servises.post_user(body.group_id, body.chat_id)
    return {"result": result}


"""put requests"""


@app.put("/faculties/{id}")
def faculty(id: int, body: FacultyBody):
    result = faculty_servises.put_faculty(id, body.name)
    return {"result": result}


@app.put("/courses/{id}")
def course(id: int, body: CourseBody):
    result = course_servises.put_course(id, body.num)
    return {"result": result}


@app.put("/forms/{id}")
def form(id: int, body: FormBody):
    result = form_servises.put_form(id, body.type)
    return {"result": result}


@app.put("/groups/{id}")
def group(id: int, body: GroupBody):
    result = group_servises.put_group(id, body.name, body.faculty_id, body.course_id, body.form_id)
    return {"result": result}


@app.put("/users/{id}")
def user(id: int, body: UserBody):
    result = user_servises.put_user(id, body.chat_id, body.group_id)
    return {"result": result}


"""delete all requests"""


@app.delete("/faculties/all")
def faculty():
    result = faculty_servises.delete_all_faculties()
    return {"result": result}


@app.delete("/courses/all")
def course():
    result = course_servises.delete_all_courses()
    return {"result": result}


@app.delete("/forms/all")
def form():
    result = form_servises.delete_all_forms()
    return {"result": result}


@app.delete("/groups/all")
def group():
    result = group_servises.delete_all_groups()
    return {"result": result}


@app.delete("/users/all")
def user():
    result = user_servises.delete_all_users()
    return {"result": result}


@app.delete("/users/sorted")
def user(body: UserBody):
    result = user_servises.delete_user_sorted(body.chat_id, body.group_id)
    return {"result": result}


"""delete one requests"""


@app.delete("/faculties/{id}")
def faculty(id: int):
    result = faculty_servises.delete_faculty(id)
    return {"result": result}


@app.delete("/courses/{id}")
def course(id: int):
    result = course_servises.delete_course(id)
    return {"result": result}


@app.delete("/forms/{id}")
def form(id: int):
    result = form_servises.delete_form(id)
    return {"result": result}


@app.delete("/groups/{id}")
def group(id: int):
    result = group_servises.delete_group(id)
    return {"result": result}


@app.delete("/users/{id}")
def user(id: int):
    result = user_servises.delete_user(id)
    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(
        "control:app",
        host='localhost',
        port=8000,
        reload=True
    )
