from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = None;

def initialize_database(DATABASE_URL):

    global engine  
    engine = create_engine(DATABASE_URL)
    
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)

def get_db():
    
    global engine  
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()