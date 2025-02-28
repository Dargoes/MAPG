from pydantic import BaseModel, EmailStr
from fastapi import Form


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @classmethod
    def form(
        cls, username: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)
    ):
        return cls(username=username, email=email, password=password)