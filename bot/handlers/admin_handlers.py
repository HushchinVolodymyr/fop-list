from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.exc import SQLAlchemyError
from database.models.fop_tov import Organiztions
from database.database import session

from app import bot
from FSM.FSM_add_fop_tov import Add_tov_fop_FSM, Refactor
from keyboards.inline_murkup import (cancel_inline, main_menu, create_admin_organization_list_markup,
                                         create_refactor_list_markup)

admin_router = Router()


## Form to get information about organization ( Check callback data that equals "fop_tov_add" )##
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

    organizations = session.query(Organiztions.edrpoy_code).all()
    organizations_edrpoy = [organization[0] for organization in organizations]

    if msg.text in organizations_edrpoy:
        await bot.send_message(msg.from_user.id, "Данна організація наявна у базі данних!", reply_markup=main_menu)
        await state.clear()
    else:
        await state.update_data(edrpoy_code=msg.text)
        await state.set_state(Add_tov_fop_FSM.cont_name)
        await bot.send_message(msg.from_user.id, "Введіть ПІБ контаку:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.cont_name)
async def add_fop_tov_company_name(msg: Message, state: FSMContext):
    await state.update_data(cont_name=msg.text)
    await state.set_state(Add_tov_fop_FSM.cont_phone_number)
    await bot.send_message(msg.from_user.id, "Введіть номер телефону контакту:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.cont_phone_number)
async def add_fop_tov_cont_phone_number(msg: Message, state: FSMContext):
    await state.update_data(cont_phone_number = msg.text)
    await state.set_state(Add_tov_fop_FSM.email)
    await bot.send_message(msg.from_user.id, "Введіть єлектронну пошту контакту:", reply_markup=cancel_inline)


@admin_router.message(Add_tov_fop_FSM.email)
async def add_fop_tov_email(msg: Message, state:FSMContext):
    await state.update_data(email = msg.text)
    await state.set_state(Add_tov_fop_FSM.adress)
    await bot.send_message(msg.from_user.id, "Введіть адресу контаку:", reply_markup=cancel_inline)


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

    await bot.send_message(msg.from_user.id, "Організація успішно додана до бази даних✅",
                           reply_markup = main_menu)

#########################################################################################


##################### Functiom to get list menu of organization ##########################
@admin_router.callback_query(lambda c: c.data == "refactor")
async def org_list(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    object_id = 1

    try:
        organization = session.query(Organiztions).filter_by(id=object_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних⛔", reply_markup=main_menu)
    finally:
        session.close()

    reply = create_admin_organization_list_markup(object_id)

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


## Refactor Organizztion ( Check callback data that starts with "refactor_organization:" ) ##
@admin_router.callback_query(lambda c: c.data.startswith("refactor_organization:"))
async def refactor(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    object_id = callback_query.data.split(":")[1]

    try:
        organization = session.query(Organiztions).filter_by(id=object_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних⛔", reply_markup=main_menu)
    finally:
        session.close()


    reply = create_refactor_list_markup(object_id)

    link_edrpoy = f"<a href='https://clarity-project.info/tenderer/{organization.edrpoy_code}'>{organization.edrpoy_code}</a>"

    await bot.send_message(user_id, f"📍Назва компанії:    {organization.company_name}\n\n"
                                    f"📍Код ЄДРПОУ:    {link_edrpoy}\n\n"
                                    f"📍ПІБ контактної особи:    {organization.cont_name}\n\n"
                                    f"📍Телефон контактної особи:    {organization.cont_phone_number}\n\n"
                                    f"📍Електрона пошта:    {organization.email}\n\n"
                                    f"📍Адреса:    {organization.adress}\n\n"
                                    f"📍Нотатка: {organization.notion}\n\n"
                                    f"Оберыть графу для редагування",
                                    parse_mode='HTML',
                                    reply_markup=reply)


## Refactor ( Check callback data that starts with "ref:" ) ##
@admin_router.callback_query(lambda c: c.data.startswith("ref:"))
async def refactor_element(callback_data: CallbackQuery, state: FSMContext):
    user_id = callback_data.from_user.id
    object_id = callback_data.data.split(":")[2]
    element = callback_data.data.split(":")[1]

    await state.set_state(Refactor.refactor)
    await state.update_data(element = element, object_id = object_id)
    await bot.send_message(user_id, "Введіть нове значення:")

@admin_router.message(Refactor.refactor)
async def set_reafctor_element(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    element = data.get("element")
    object_id = data.get("object_id")
    new_element = msg.text

    try:
        refactor_element = session.query(Organiztions).filter_by(id=object_id).first()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних⛔", reply_markup=main_menu)
    finally:
        session.close()

    setattr(refactor_element, element, new_element)

    try:
        session.commit()
        await bot.send_message(user_id, "Значення оновленне✅", reply_markup=main_menu)
    except SQLAlchemyError as e:
        session.rollback()
        await bot.send_message(user_id, "Помилка запису о бази данних!⛔", reply_markup=main_menu)
        print(f"ERROR: {e}")
    finally:
        session.close()

    await state.clear()

##########################################################################################################


## Delete organization ( Check callback data that starts with "delete_organization:" ) ##
@admin_router.callback_query(lambda c: c.data.startswith("delete_organization:"))
async def delete_organization(callback_query: CallbackQuery):
    object_id = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id


    try:
        organiztion = session.query(Organiztions).get(object_id)
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
        await bot.send_message(user_id, "Помилка пошуку організації у базі даних⛔", reply_markup=main_menu)
    finally:
        session.close()

    try:
        session.delete(organiztion)
        session.commit()
        await bot.send_message(user_id, f"Організація:    {organiztion.company_name}\n\n"
                                        f"Успішно видалена с бд✅",
                                        reply_markup=main_menu)
        organizations = session.query(Organiztions).order_by(Organiztions.id).all()

        for index, organization in enumerate(organizations, start=1):
            organization.id = index

        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        await bot.send_message(user_id, "Помилка видалення з бази данних!⛔", reply_markup=main_menu)
        print(f"ERROR: {e}")
    finally:
        session.close()




