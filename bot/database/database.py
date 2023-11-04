import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

engine = create_engine('sqlite:///main.db',  echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()



def create_db():
    Base.metadata.create_all(engine)








