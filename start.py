import json
import asyncio
from unittest.mock import call

from config import bot
from aiogram import types, Router
from aiogram.filters import Command
from keyboards.inline import start_menu
from trans import translations

router = Router()

# def save_user(user_id, language_code):
#     with open('data.json', 'r+') as f:
#         data = json.load(f)
#         data["users"][str(user_id)] = language_code
#         f.seek(0)
#         json.dump(data, f, ensure_ascii=False, indent=3)
#
# def get_user(user_id):
#     with open('data.json', 'r') as f:
#         data = json.load(f)
#         return data["users"].get(str(user_id))
#



# команда старт
@router.message(Command("start"))
async def start_command(message: types.Message):

    await message.answer(translations["chat"]["start"],
                         reply_markup=start_menu())








