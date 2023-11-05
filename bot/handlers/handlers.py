from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.models.users import User
from bot.database.database import session
from sqlalchemy.exc import SQLAlchemyError

router = Router()


@router.message(Command('start'))
async def start_handler(msg : Message):
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


    await msg.answer("main router")


