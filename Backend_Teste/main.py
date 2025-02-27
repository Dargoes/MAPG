from fastapi import FastAPI, Form, Request
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def root():
    return {'message': 'Mensagem recebida com sucesso!'}

@app.post("/registro")
def exibir_dados(request: Request, name:str = Form(), email:EmailStr = Form(), password:str = Form()):
    return templates.TemplateResponse("registro.html", {
        "request": request,
        "message": 'Dados Recebidos',
        "name": name,
        "email": email,
        "password": password
    })

@app.post("/login")
def exibir_dados(request: Request, email:EmailStr = Form(), password:str = Form()):
    return templates.TemplateResponse("registro.html", {
        "request": request,
        "message": 'Login efetuado!',
        "email": email,
        "password": password
    })