from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from sqlalchemy.exc import SQLAlchemyError
from bot.database.models.users import User
from bot.database.models.fop_tov import Organiztions
from bot.database.database import session

from bot.app import bot
from bot.FSM.FSM_add_fop_tov import Add_tov_fop_FSM
from bot.keyboards.inline_murkup import cancel_inline, refactor_organization

admin_router = Router()



############### Form to get information about organization#########
@admin_router.callback_query(lambda c: c.data == "fop_tov_add")
async def fop_tov_add_handler(msg: Message, state: FSMContext):
    await state.set_state(Add_tov_fop_FSM.company_name)
    await bot.send_message(msg.from_user.id, "Введіть назву компанії:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.company_name)
async def add_fop_tov_company_name(msg: Message, state: FSMContext):
    await state.update_data(company_name = msg.text)
    await state.set_state(Add_tov_fop_FSM.edrpoy_code)
    await bot.send_message(msg.from_user.id, "Введіть код ЄДРПОУ:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.edrpoy_code)
async def add_fop_tov_edrpoy(msg: Message, state: FSMContext):

    organizations = session.Query(Organiztions.edrpoy_code).all()
    organizations_edrpoy = [organization[0] for organization in organizations]

    if msg.text in organizations_edrpoy:
        await bot.send_message(msg.from_user.id, "Данна організація наявна у базі данних!")
        await state.clear()
    else:
        await state.update_data(edrpoy_code=msg.text)
        await state.set_state(Add_tov_fop_FSM.cont_name)
        await bot.send_message(msg.from_user.id, "Введіть ПІБ контаку:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.cont_name)
async def add_fop_tov_company_name(msg: Message, state: FSMContext):
    await state.update_data(cont_name=msg.text)
    await state.set_state(Add_tov_fop_FSM.cont_phone_number)
    await bot.send_message(msg.from_user.id, "Введіть номер контакту:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.cont_phone_number)
async def add_fop_tov_cont_phone_number(msg: Message, state: FSMContext):
    await state.update_data(cont_phone_number = msg.text)
    await state.set_state(Add_tov_fop_FSM.email)
    await bot.send_message(msg.from_user.id, "Введіть єлектронну пошту контакту:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.email)
async def add_fop_tov_email(msg: Message, state:FSMContext):
    await state.update_data(email = msg.text)
    await state.set_state(Add_tov_fop_FSM.adress)
    await bot.send_message(msg.from_user.id, "Введіть адресу контаку:")


@admin_router.message(Add_tov_fop_FSM.adress)
async def add_fop_tov_adress(msg: Message, state: FSMContext):
    data = await state.get_data()

    organization = Organiztions(data["company_name"], data["edrpoy_code"],
                                data["cont_name"], data["cont_phone_number"],
                                data["email"], msg.text)

    try:
        session.add(organization)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
    finally:
        session.close()

    await bot.send_message(msg.from_user.id, "Організація успішно додана до бази даних✅")

#########################################################################################


##################### Functiom to get list menu of organization ##########################
@admin_router.callback_query(lambda c: c.data == "refactor")
async def org_list(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Organization", reply_markup=refactor_organization)

