from fastapi import FastAPI, Form, Request, Depends
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates
from schemas import UserSchema
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI()

database = []

def convert_form_user_schema(user:str = Form(), email:EmailStr = Form(), password:str = Form()) -> UserSchema:
    client = UserSchema(user=user, email=email, password=password)
    return client

@app.get("/")
def root():
    return {'message': 'Aplicação rodando!'}

@app.post("/registro")
def create_user(request: Request, user: UserSchema = Depends(convert_form_user_schema)):
    user_id = len(database) + 1
    database.append([user_id, user.user, user.email, user.password])

    return templates.TemplateResponse("registro.html", {
        "request": request,
        "message": 'Dados Recebidos',
        "id": user_id,
        "user": user.user,
        "email": user.email,
        "password": user.password
    })

@app.post("/login")
def login_user(request: Request, user: UserSchema = Depends(convert_form_user_schema)):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": 'Login efetuado!',
        "user": user.user,
        "email": user.email,
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)