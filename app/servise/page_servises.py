from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def home(request, jwt):
    if jwt:
        pass
    else:
        return templates.TemplateResponse("index.html", {"request": request})


def log_in(request, login, password):
    return templates.TemplateResponse("login.html", {"request": request, "login": login, "password": password})
