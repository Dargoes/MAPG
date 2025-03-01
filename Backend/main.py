from fastapi_config.schemas import (Message, UserSchema)
from fastapi_config.models import User
from fastapi_config.database import get_session
from fastapi import (FastAPI, Depends, Request, Form)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
import uvicorn 
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=html_path)
css_path = os.path.join(BASE_DIR, 'static')

app = FastAPI()
app.mount("/static", StaticFiles(directory=css_path), name="static")


@app.get('/', response_model=Message)
def read_root():
    return Message(message='Aplicação Rodando!')


@app.post('/registro', status_code=201, response_class=HTMLResponse)
def create_user(request: Request, user: UserSchema = Depends(UserSchema.form), session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            return templates.TemplateResponse(request=request, name="registro_erro.html", context={
        "message": 'Dados Recebidos',
        "code": '400 Bad Request',
        "result": 'Esse usuário já existe'
    })
        elif db_user.email == user.email:
            return templates.TemplateResponse(request=request, name="registro_erro.html", context={
        "message": 'Dados Recebidos',
        "code": '400 Bad Request',
        "result": 'Esse email já existe'
    })
        
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return templates.TemplateResponse(request=request, name="profile.html", context={
        "message": 'Dados Recebidos',
        "user": db_user.username,
        "email": "*" * len(db_user.email),
        "password": "*" * len(db_user.password),
        "create_at": db_user.created_at,
        "user_id": db_user.id
    })


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.email == email) & (User.password == password)))
    
    if db_user is None:
        return templates.TemplateResponse(request=request, name="registro_erro.html", context={
        "message": 'Dados Recebidos',
        "code": '404 Not Found',
        "result": 'O usuário não foi encontrado'
    })
    
    # Se tudo estiver certo, retorne uma resposta de sucesso
    return templates.TemplateResponse(request=request, name="profile.html", context={
        "message": 'Dados Recebidos',
        "user": db_user.username,
        "email": "*" * len(db_user.email),
        "password": "*" * len(db_user.password),
        "create_at": db_user.created_at,
        "user_id": db_user.id
    })


@app.post('/delete', response_model=Message)
def delete_user(request: Request, user_id: int = Form(...), session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        return templates.TemplateResponse(request=request, name="registro_erro.html", context={
        "message": 'Dados Recebidos',
        "code": '404 Not Found',
        "result": 'O usuário não foi encontrado'
    })
    
    session.delete(db_user)
    session.commit()

    return templates.TemplateResponse(request=request, name="registro_erro.html", context={
        "message": 'Dados Recebidos',
        "code": '200 OK',
        "result": 'Usuário deletado com sucesso'
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)