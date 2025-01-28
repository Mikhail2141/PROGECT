import asyncio
from aiogram import Dispatcher
from config import bot, dp
import start, main_menu


# Регистрируем все обработчики
dp.include_router(start.router)
dp.include_router(main_menu.router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
