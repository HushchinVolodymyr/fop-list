import asyncio

from handlers.handlers import router
from handlers.admin_handlers import admin_router

from app import bot, dp


async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())