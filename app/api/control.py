from typing import List

from fastapi import Request, Response

from api.schemas import TokenSchema, UserSchema, GroupSchema, FacultySchema, CourseSchema, FormSchema, GroupUserSchema
from main import app
from models.user import UserRole
from servise import faculty_servises, course_servises, form_servises, group_servises, user_servises, auth


@app.post("/token", response_model=TokenSchema)
async def login_for_access_token(body: UserSchema, response: Response):
    result = auth.login_for_access_token(body.username, body.password)
    print(result)
    response.set_cookie(key="access_token", value=result["access_token"])
    return result


@app.delete("/token")
async def sign_out(response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"result": "signed out"}


@app.get("/")
def read_root() -> dict:
    return {"hello": "world"}


@app.get("/admin")
async def home(request: Request):
    if auth.check_role(request.cookies, UserRole.moderator.value):
        return request.cookies


@app.get("/faculties/all")
async def faculty(mark: str = "name"):
    return faculty_servises.get_all_faculties(mark)


@app.get("/group_users/all")
async def user_group():
    return group_servises.get_all_link()


@app.get("/courses/all")
async def course():
    return course_servises.get_courses()


@app.get("/forms/all")
async def form():
    return form_servises.get_all_forms()


@app.get("/groups/all")
async def group():
    return group_servises.get_groups(mark="name")


@app.get("/groups/sorted")
async def group(body: GroupSchema):
    return group_servises.get_groups(name=body.name, faculty_id=body.faculty_id, course_id=body.course_id,
                                     form_id=body.form_id)


@app.get("/users/all")
async def user(request: Request):
    if auth.check_role(request.cookies, UserRole.moderator.value):
        return user_servises.get_users()


"""get one requests"""


@app.get("/faculties/{faculty_id}")
async def faculty(faculty_id: int):
    return faculty_servises.get_one_faculty(faculty_id)


@app.get("/courses/{course_id}")
async def course(course_id: int):
    return course_servises.get_course(course_id)


@app.get("/group_users/by_group/{group_id}")
async def user_group(group_id: int):
    return group_servises.get_all_link(group_id=group_id)


@app.get("/group_users/by_user/{user_id}")
async def user_group(user_id):
    return group_servises.get_all_link(user_id=user_id)


@app.get("/forms/{form_id}")
async def form(form_id: int):
    return form_servises.get_one_form(form_id)


@app.get("/groups/{group_id}")
async def group(group_id: int):
    return group_servises.get_group(group_id)


@app.get("/users/by_chat/{chat_id}")
async def user(chat_id):
    return user_servises.get_user(chat_id=chat_id)


"""post requests"""


@app.post("/faculties/list")
async def faculty(bodies: List[FacultySchema], request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        names = [body.name for body in bodies]
        result = faculty_servises.post_list_of_faculties(names)
        return {"result": result}


@app.post("/faculties")
async def faculty(body: FacultySchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = faculty_servises.post_faculty(body.name)
        return {"result": result}


@app.post("/courses")
async def course(body: CourseSchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = course_servises.post_course(body.num)
        return {"result": result}


@app.post("/forms")
async def form(body: FormSchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = form_servises.post_form(body.type)
        return {"result": result}


@app.post("/users/")
async def user(body: UserSchema) -> dict:
    result = user_servises.post_user(body.chat_id, body.username, body.password)
    return {"result": result}


@app.post("/groups")
async def group(body: GroupSchema) -> dict:
    result = group_servises.post_group(body.name, body.faculty_id, body.course_id, body.form_id, body.status_code)
    return {"result": result}


@app.post("/group_users")
async def user_group(body: GroupUserSchema) -> dict:
    result = group_servises.post_group_user(user_id=body.user_id, group_id=body.group_id)
    return {"result": result}


"""put requests"""


@app.put("/faculties/{faculty_id}")
async def faculty(faculty_id: int, body: FacultySchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = faculty_servises.put_faculty(faculty_id, body.name)
        return {"result": result}


@app.put("/courses/{course_id}")
async def course(course_id: int, body: CourseSchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = course_servises.put_course(course_id, body.num)
        return {"result": result}


@app.put("/groups/approve/all")
async def groups(request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = group_servises.approve_all_waiting_groups()
        return {"result": result}


@app.put("/forms/{form_id}")
async def form(form_id: int, body: FormSchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = form_servises.put_form(form_id, body.type)
        return {"result": result}


@app.put("/groups/{group_id}")
async def group(group_id: int, body: GroupSchema, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = group_servises.put_group(group_id, body.name, body.faculty_id, body.course_id, body.form_id,
                                          body.status_code)
        return {"result": result}


"""delete all requests"""


@app.delete("/faculties/all")
async def faculty(request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = faculty_servises.delete_all_faculties()
        return {"result": result}


@app.delete("/courses/all")
async def course(request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = course_servises.delete_all_courses()
        return {"result": result}


@app.delete("/forms/all")
async def form(request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = form_servises.delete_all_forms()
        return {"result": result}


@app.delete("/groups/all")
async def group(request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = group_servises.delete_all_groups()
        return {"result": result}


"""delete one requests"""


@app.delete("/faculties/{faculty_id}")
async def faculty(faculty_id: int, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = faculty_servises.delete_faculty(faculty_id)
        return {"result": result}


@app.delete("/courses/{course_id}")
async def course(course_id: int, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = course_servises.delete_course(course_id)
        return {"result": result}


@app.delete("/users/{user_id}")
async def user(user_id: int, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = user_servises.delete_user_by_id(user_id)
        return {"result": result}


@app.delete("/forms/{form_id}")
async def form(form_id: int, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = form_servises.delete_form(form_id)
        return {"result": result}


@app.delete("/groups/{group_id}")
async def group(group_id: int, request: Request) -> dict:
    if auth.check_role(request.cookies, UserRole.moderator.value):
        result = group_servises.delete_group(group_id)
        return {"result": result}


@app.delete("/group_users")
async def group_user(body: GroupUserSchema) -> dict:
    result = group_servises.delete_group_user(body.user_id, body.group_id)
    return {"result": result}
