from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from settings import Settings


engine = create_engine(Settings().DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session