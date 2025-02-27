from fastapi import FastAPI, Form, Request
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates
import uvicorn

templates = Jinja2Templates(directory="templates")

app = FastAPI()

database = []

@app.get("/")
def root():
    return {'message': 'Mensagem recebida com sucesso!'}

@app.post("/registro")
def create_user(request: Request, user:str = Form(), email:EmailStr = Form(), password:str = Form()):
    user_id = len(database) + 1
    database.append([user_id, user, email, password])

    return templates.TemplateResponse("registro.html", {
        "request": request,
        "message": 'Dados Recebidos',
        "id": user_id,
        "user": user,
        "email": email,
        "password": password
    })

@app.post("/login")
def login_user(request: Request, email:EmailStr = Form(), password:str = Form()):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": 'Login efetuado!',
        "email": email,
        "password": password
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)