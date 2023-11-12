import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.models.fop_tov import Organiztions
from database.models.users import User

engine = create_engine('sqlite:///main.db',  echo=False)

Organiztions.__table__.create(bind=engine, checkfirst=True)
User.__table__.create(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()
