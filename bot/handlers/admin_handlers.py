from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from sqlalchemy.exc import SQLAlchemyError
from bot.database.models.users import User
from bot.database.database import session

admin_router = Router()


@admin_router.message(Command('admin_start'))
async def admin_start_handler(msg : Message):
    username = msg.from_user.username
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    user_admin = True

    user = User(username, user_id, first_name, last_name, user_admin)

    try:
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERROR: {e}")
    finally:
        session.close()



    await msg.answer(f"Username: {username}\nUser id: {user_id}\n"
                     f"User first and last name: {first_name} {last_name}")