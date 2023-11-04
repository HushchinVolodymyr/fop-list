from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Organiztions(Base):
    __tablename__ = 'FOP_TOV'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_name = Column(String, nullable=False)
    edrpoy_code = Column(Integer, nullable=False)
    cont_name = Column(String, nullable=False)
    cont_phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    adress = Column(String, nullable=False)
    is_checked = Column(Boolean, nullable=False, default=False)
    notion = Column(String, nullable=True)

    def __init__(self, company_name: str, edrpoy_code: int, cont_name: str,
                 cont_phone_number: str, email: str, adress: str):
        self.company_name = company_name
        self.edrpoy_code = edrpoy_code
        self.cont_name = cont_name
        self.cont_phone_number = cont_phone_number
        self.email = email
        self.adress = adress

    def __repr__(self):
        return f"ЄДРПОУ: {self.edrpoy_code}, Назва компанії: {self.company_name}."