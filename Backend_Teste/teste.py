from models import User, table_registry
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def test():
    engine = create_engine(
        'sqlite:///database.db'
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            username='dunossauro', 
            password='123', 
            email='duno@gmail.com'
            )
        
        session.add(user)
        session.commit()
        session.refresh(user)

test()

