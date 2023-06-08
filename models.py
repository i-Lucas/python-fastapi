from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MVP_Table(Base):
    __tablename__ = "mvp_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class ItemCreate(BaseModel):
    name: str