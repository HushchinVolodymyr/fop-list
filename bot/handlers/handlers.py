from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database.models.users import User
from database.models.fop_tov import Organiztions
from database.database import session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from keyboards.inline_murkup import (admin_menu, main_menu,
                                         user_menu, create_admin_organization_list_markup,
                                         create_user_organization_list_markup)
from app import bot
from FSM.FSM_add_fop_tov import Get_edrpoy, Get_notion

# Create router for user handlers
router = Router()


## Start handler ( Check all sended message and reatc on command "/start" ) ##
@router.message(Command('start'))
async def start_handler(msg: Message):
    user_id = msg.from_user.id

    users = session.query(User.user_id).all()
    users_id = [user[0] for user in users]

    if user_id not in users_id:
        user = User(msg.from_user.username, msg.from_user.id,
                    msg.from_user.first_name, msg.from_user.last_name)

        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"ERROR: {e}")
            await msg.answer("Користувача не можливо зарееструвати або його не має у базі даних!")
        finally:
            session.close()

    try:
        user = session.query(User).filter_by(user_id = user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"EROR: {e}")
        await msg.answer("Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user.user_admin:
        reply_markup = admin_menu
    else:
        reply_markup = user_menu

    await msg.answer("Меню:\nОберіть шо вас цікавить", reply_markup = reply_markup)


## Cancel handler ( Check callback data that equals "cancel" )###
@router.callback_query(lambda c: c.data == "cancel")
async def cancel(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user.user_admin:
        reply_markup = admin_menu
    else:
        reply_markup = user_menu

    await (bot.send_message(user_id, "Меню:\nОберіть шо вас цікавить",
                                reply_markup=reply_markup))




## Return to main menu handler ( Check callback data that equals "main_menu" ) ##
@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu_call(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user.user_admin:
        reply_markup = admin_menu
    else:
        reply_markup = user_menu

    await bot.send_message(user_id, "Меню:\nОберіть шо вас цікавить",
                     reply_markup=reply_markup)



## Find by EDPROY handler ( Check callback data that equals "find_by_edrpoy" )##
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
        session.rollback()
        print(f"ERROR: {e}")
        await msg.answer("Помилка пошуку організації у базі даних", reply_markup=main_menu)
    finally:
        session.close()

    link_edrpoy = f"<a href='https://clarity-project.info/tenderer/{organization.edrpoy_code}'>{organization.edrpoy_code}</a>"

    await msg.answer(f"📍Назва компанії:    {organization.company_name}\n\n"
                     f"📍Код ЄДРПОУ:    {link_edrpoy}\n\n"
                     f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                     f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                     f"📍Електрона пошта:    {organization.email}\n\n"
                     f"📍Адреса:    {organization.adress}\n\n"
                     f"📍Нотатка: {organization.notion}",
                     parse_mode="HTML",
                     reply_markup=main_menu)
    await state.clear()

##########################################################################

## Organization list ( Check callback data that equals "organization" )##
@router.callback_query(lambda c: c.data == "organization")
async def organizations_list(callback_query: CallbackQuery):
    org_id = 1
    user_id = callback_query.from_user.id
    organization = None

    while organization is None:
        try:
            organization = session.query(Organiztions).filter_by(id = org_id).first()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"ERROR: {e}")
            await bot.send_message(user_id, "Помилка пошуку організації у базі даних", reply_markup=main_menu)
        finally:
            session.close()

        if organization.is_checked:
            organization = None
            org_id += 1

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user and user.user_admin:
        reply = create_admin_organization_list_markup(org_id)
    else:
        reply = create_user_organization_list_markup(org_id)

    link_edrpoy = f"<a href='https://clarity-project.info/tenderer/{organization.edrpoy_code}'>{organization.edrpoy_code}</a>"

    await bot.send_message(user_id, f"📍Назва компанії:    {organization.company_name}\n\n"
                    f"📍Код ЄДРПОУ:    {link_edrpoy}\n\n"
                    f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                    f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                    f"📍Електрона пошта:    {organization.email}\n\n"
                    f"📍Адреса:    {organization.adress}\n\n"
                    f"📍Нотатка: {organization.notion}",
                    parse_mode='HTML',
                    reply_markup=reply)

## Organization forward list ( Check callback data that starts with "forward_organization:" )##
@router.callback_query(lambda c: c.data.startswith("forward_organization:"))
async def forward_org_list(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    count_of_organization = session.query(func.count(Organiztions.id)).scalar()

    object_id = int(callback_query.data.split(":")[1])

    organization = None

    while organization is None:
        try:
            organization = session.query(Organiztions).filter_by(id=object_id).first()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"ERROR: {e}")
            await bot.send_message(user_id, "Помилка пошуку організації у базі даних", reply_markup=main_menu)
        finally:
            session.close()

        if organization:
            if organization.is_checked:
                organization = None
                object_id += 1
        else:
            object_id += 1

        if object_id > count_of_organization:
            break

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user and user.user_admin:
        reply_markup = create_admin_organization_list_markup(object_id)
    else:
        reply_markup = create_user_organization_list_markup(object_id)

    if organization is not None:
        link_edrpoy = f"<a href='https://clarity-project.info/tenderer/{organization.edrpoy_code}'>{organization.edrpoy_code}</a>"

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                        text=f"📍Назва компанії:    {organization.company_name}\n\n"
                        f"📍Код ЄДРПОУ:    {link_edrpoy}\n\n"
                        f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                        f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                        f"📍Електрона пошта:    {organization.email}\n\n"
                        f"📍Адреса:    {organization.adress}\n\n"
                        f"📍Нотатка: {organization.notion}",
                        parse_mode='HTML',
                        reply_markup=reply_markup)
    else:
        await bot.send_message(user_id, "Ви пролистали усі організації", reply_markup=main_menu)


## Organization back list ( Check callback data that starts with "back_organization:" )##
@router.callback_query(lambda c: c.data.startswith("back_organization:"))
async def back_org_list(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    object_id = int(callback_query.data.split(":")[1])

    organization = None

    while organization is None:
        try:
            organization = session.query(Organiztions).filter_by(id=object_id).first()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"ERROR: {e}")
            await bot.send_message(user_id, "Помилка пошуку організації у базі даних", reply_markup=main_menu)
        finally:
            session.close()

        if organization:
            if organization.is_checked:
                organization = None
                object_id -= 1
        else:
            object_id -= 1

        if object_id < 0:
            break

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Користувача не має у базі даних!", reply_markup=main_menu)
    finally:
        session.close()

    if user and user.user_admin:
        reply_markup = create_admin_organization_list_markup(object_id)
    else:
        reply_markup = create_user_organization_list_markup(object_id)

    if organization:
        link_edrpoy = f"<a href='https://clarity-project.info/tenderer/{organization.edrpoy_code}'>{organization.edrpoy_code}</a>"

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                        text=f"📍Назва компанії:    {organization.company_name}\n\n"
                        f"📍Код ЄДРПОУ:    {link_edrpoy}\n\n"
                        f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                        f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                        f"📍Електрона пошта:    {organization.email}\n\n"
                        f"📍Адреса:    {organization.adress}\n\n"
                        f"📍Нотатка: {organization.notion}",
                        parse_mode='HTML',
                        reply_markup=reply_markup)
    else:
        await bot.send_message(user_id, "Ви переглянули усі організації", reply_markup=main_menu)


###############################################################################


## Notion ( Check callback data that starts with "notion:" )##
@router.callback_query(lambda c: c.data.startswith("notion:"))
async def make_notion(callback_query: CallbackQuery, state: FSMContext):
    object_id = callback_query.data.split(":")[1]

    await state.set_state(Get_notion.id)
    await state.update_data(id = object_id)
    await state.set_state(Get_notion.notion)
    await bot.send_message(callback_query.from_user.id,
                           "Введіть нотатку:")


@router.message(Get_notion.notion)
async def set_notion(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()

    object_id = data.get("id")

    print(object_id)

    try:
        organization = session.query(Organiztions).filter_by(id=object_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних", reply_markup=main_menu)
    finally:
        session.close()

    organization.notion = msg.text

    try:
        session.add(organization)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка с додаванням нотатки до бази даних!⛔", reply_markup=main_menu)
    finally:
        session.close()

    await bot.send_message(user_id, "Нотатка успішно додана!✅",reply_markup=main_menu)


###########################################################################################

## Hide organization ( Check callback data that starts with "not_show:" )##
@router.callback_query(lambda c: c.data.startswith("not_show:"))
async def hide(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    object_id = callback_query.data.split(":")[1]

    try:
        organization = session.query(Organiztions).filter_by(id=object_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних", reply_markup=main_menu)
    finally:
        session.close()

    organization.is_checked = True

    try:
        session.add(organization)
        session.commit()
        await bot.send_message(callback_query.from_user.id,
                               f"Організація:    {organization.company_name}\n\n"
                               f"Код ЕДРПОУ:    {organization.edrpoy_code}\n\n"
                               f"Скрита у списку для перегляду!✅", reply_markup=main_menu)
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка у скриті організації!⛔", reply_markup=main_menu)
    finally:
        session.close()

##########################################################################################