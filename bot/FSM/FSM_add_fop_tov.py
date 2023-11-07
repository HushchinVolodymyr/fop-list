from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Add_tov_fop_FSM(StatesGroup):
    company_name = State()
    edrpoy_code = State()
    cont_name = State()
    cont_phone_number = State()
    email = State()
    adress = State()


class Get_edrpoy(StatesGroup):
    edrpoy = State()