from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.models.users import User
from bot.database.models.fop_tov import Organiztions
from bot.database.database import session
from sqlalchemy.exc import SQLAlchemyError

from bot.keyboards.inline_murkup import admin_menu, cancel_inline, main_menu, start_menu
from bot.app import bot
from bot.FSM.FSM_add_fop_tov import Get_edrpoy

router = Router()


############## Start handler ############################
@router.message(Command('start'))
async def start_handler(msg: Message):
    username = msg.from_user.username
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name

    users = session.query(User.user_id).all()
    users_id = [user[0] for user in users]

    if user_id not in users_id:
        user = User(username, user_id, first_name, last_name)

        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"EROR: {e}")
        finally:
            session.close()

    user = session.query(User).filter_by(user_id = user_id).first()

    if user.user_admin:
        reply = admin_menu
    else:
        reply = start_menu

    await msg.answer("Меню:\nОберіть шо вас цікавить",
                     reply_markup = reply)


##################### Cancel handler #######################
@router.callback_query(lambda c: c.data == "cancel")
async def cancel(state: FSMContext, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user.user_admin:
        await bot.send_message(callback_query.from_user.id, "Admin router", reply_markup=admin_menu)
        await state.clear()
    else:
        await bot.send_message(callback_query.from_user.id,"main router", reply_markup=start_menu)
        await state.clear()



#################### Return to start menu handler #####################
@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        print(f"EROR: {e}")
    finally:
        session.close()


    if user and user.user_admin:
        reply = admin_menu
    else:
        reply = start_menu

    await bot.send_message(callback_query.from_user.id, "Меню:\nОберіть шо вас цікавить",
                     reply_markup=reply)



#################### Find by EDPROY handler ##############################
@router.callback_query(lambda c: c.data == "find_by_edrpoy")
async def get_edrpoy(msg: Message, state: FSMContext):
    await state.set_state(Get_edrpoy.edrpoy)
    await bot.send_message(msg.from_user.id, "Введіть ЄДРПОУ:")


@router.message(Get_edrpoy.edrpoy)
async def find_by_edrpoy(msg: Message, state: FSMContext):
    edrpoy = msg.text

    try:
        organization = session.query(Organiztions).filter_by(edrpoy_code = edrpoy).first()
    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
    finally:
        session.close()

    await msg.answer(f"📍Назва компанії:    {organization.company_name}\n\n"
                     f"📍Код ЄДРПОУ:    {organization.edrpoy_code}\n\n"
                     f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                     f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                     f"📍Електрона пошта:    {organization.email}\n\n"
                     f"📍Адреса:    {organization.adress}\n\n",
                     reply_markup=main_menu)
    await state.clear()

##########################################################################


