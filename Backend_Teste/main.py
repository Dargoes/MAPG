from schemas import (Message, UserSchema)
from models import User
from database import get_session
from fastapi import (FastAPI, HTTPException, Depends, Request)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
import datetime
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=html_path)

css_path = os.path.join(BASE_DIR, 'static')

app = FastAPI()
app.mount("/static", StaticFiles(directory=css_path), name="static")

@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Aplicação Rodando!'}


@app.post('/registro', status_code=201, response_class=HTMLResponse)
def create_user(request: Request, user: UserSchema = Depends(UserSchema.form), session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail='Email already exists')
        
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return templates.TemplateResponse(request=request, name="profile.html", context={
        "message": 'Dados Recebidos',
        "user": db_user.username,
        "email": "*" * len(db_user.email),
        "password": "*" * len(db_user.password),
        "create_at": datetime.datetime.now()
    })

@app.delete('/delete', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    
    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted successfully'}