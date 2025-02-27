from fastapi import Form
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    user: str
    email: EmailStr
    password: str

class PublicSchema(BaseModel):
    id: int
    user: str
    email: EmailStr

def convert_form_public(user:str = Form(), email:EmailStr = Form()) -> PublicSchema:
    client = PublicSchema(user=user, email=email)
    return client