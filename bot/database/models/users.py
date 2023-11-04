from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String)
    user_id = Column(Integer)
    user_firstname = Column(String)
    user_lastname = Column(String)
    user_admin = Column(Boolean, default=False)

    def __init__(self, username: str, user_id: int, user_firstname: str,
                user_lastname: str, user_admin = False):
        self.username = username
        self.user_id = user_id
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname

        if user_admin:
            self.user_admin = user_admin


    def __repr__(self):
        return f"Username: {self.username}"