import asyncio
import datetime
import time
import gspread
import logging
from aiogram.filters.state import State,StatesGroup
from aiogram import types, Router, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from trans import translations
from keyboards.inline import (start_menu, back, buy ,dostavka, meneger,PVZ ,
                              back_buy ,  cheque , F_menu , complete , yes , No)
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re



dp = Dispatcher()
class Form(StatesGroup):
    courier_address = State()
    done = State()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Определяем маршрутизатор
router = Router()
ID  = ['1016060761']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1qhdn1BPOF0S22TsrcuDuzvPUY3RHV0IQsPwPaPwW8dE'
SERVICE_ACCOUNT_FILE = 'C:/Users/jak/PycharmProjects/pythonProject/botTech/handlers/table.json'



input_article = None # Объявляем глобальную переменную для хранения артикула товара
input_addres = None # Объявляем глобальную переменную для хранения адреса доставки

async def send_message_with_keyboard(call, text, keyboard):
    await call.message.answer(text=text, reply_markup=keyboard)
    await call.answer()


@router.callback_query(lambda call: call.data == "help")
async def help_command(call: types.CallbackQuery):
    lang_code = call.from_user.id
    help_text = translations[lang_code]["help_text"]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=translations[lang_code]["start"], callback_data="link")
        ],
        [
            InlineKeyboardButton(text=translations[lang_code]["back_to_menu"], callback_data="back_to_main_menu")
        ]
    ])
    image_url = "*"
    await call.message.answer_photo(photo=image_url, caption=f"{help_text}\n\n",
                                    reply_markup=keyboard)

@router.callback_query(lambda call: call.data == "start_menu")
async def start_menu_chat(call: types.CallbackQuery):

    lang_code = call.from_user.id

    await send_message_with_keyboard(call,
                                          f"\n{translations["chat"]["start"]}\n",
                                          start_menu())


#Кнопка FAQ
@router.callback_query(lambda call: call.data == "faq")
async def faq(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.message.delete()
    await send_message_with_keyboard(call,
                                     f"\n{translations["chat"]['F_tolk']}\n", F_menu())


@router.callback_query(lambda call: call.data.startswith("DB"))
async def DB_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['faq_DB']}",
        reply_markup=back()
    )



@router.callback_query(lambda call: call.data.startswith("VO"))
async def VO_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['faq_VO']}",
        reply_markup=back()
    )
@router.callback_query(lambda call: call.data.startswith("K"))
async def K_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['faq_K']}",
        reply_markup=back()
    )

@router.callback_query(lambda call: call.data.startswith("RK"))
async def RK_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['faq_RK']}",
        reply_markup=back()
    )



#Кнопка задать вопрос
@router.callback_query(lambda call: call.data == "ask")
async def ask_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.message.delete()
    await send_message_with_keyboard(call,
                                     f"\n{translations["chat"]['question']}\n", meneger())



@router.callback_query(lambda call: call.data.startswith("artikul"))
async def artikul_reply(call: types.CallbackQuery):

    lang_code = call.from_user.id

    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['send_artikul']}",
        reply_markup=back()
    )

pattern = r'^\d{3}$'


@router.message(lambda msg: re.search(pattern, msg.text) is not None)
async def process(msg: types.Message):
    global input_article  # Используем глобальную переменную
    lang_code = msg.from_user.id
    input_article = msg.text  # Сохраняем входящее сообщение

    if re.search(pattern, msg.text):
        product_info = get_product_info(input_article)
        if product_info:
            text = f"Фото: {product_info['photo']}\nНазвание: {product_info['name']}\nЦена: {product_info['price']} руб."
            await msg.answer(text=text, reply_markup=buy())
        else:
            text_ = "Артикул не найден"
            await msg.answer(text=text_)
    else:
        await msg.answer("Пожалуйста, введите корректный артикул.")

def get_product_info(article):
    logger.debug(f"Переданный артикул: {article}")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    range_name = f'Лист1!A:D'
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        return None
    article_column = 2  # Третья колонка (индекс 2)
    for row in values[1:]:  # Начинаем с второй строки (заголовки)
        if str(row[article_column]) == article:
            return {
                'photo': row[0],  # Фото в первой колонке
                'name': row[1],
                'article': row[article_column],
                'price': float(row[3])
            }

    return None

pat = r'^^[А-Я].{1,}$'
@router.message(lambda msg: re.search(pat, msg.text) is not None)
async def process_address(msg: types.Message):
    global input_addres
    lang_code = msg.from_user.id
    input_addres = msg.text  # Сохраняем входящее сообщение

    if re.search(pat, msg.text):
        await msg.answer(text=f"Получен адрес: {input_addres}")
        await msg.answer(text="Нажми чтобы сгенерировать чек!", reply_markup=cheque())
    else:
        await msg.answer(text="Адрес не найден!")

@router.callback_query(lambda call: call.data.startswith("Buy"))
async def artikul_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id

    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['Buy_tovar']}",
        reply_markup=dostavka()
    )


@router.callback_query(lambda call: call.data.startswith("courier"))
async def artikul_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id

    await call.bot.send_message(
        chat_id = call.message.chat.id,
        text = f"{translations['chat']['courier_']}",
        reply_markup = back_buy()
    )



@router.callback_query(lambda call: call.data.startswith("pvz"))
async def artikul_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['pvz_']}",
        reply_markup=PVZ()
    )


@router.callback_query(lambda call: call.data.startswith("chek"))
async def generate_cheque(call: types.CallbackQuery):
    lang_code = call.from_user.id
    product_info = get_product_info(input_article)  # Используем глобальную переменную



    if product_info:
        cheque_text = f"""
🎁 Ваш чек!

📅 Дата: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M"):<30}

🛠️ Товар: {product_info['name']:<40}
🔍 Артикул товара: {input_article:<20}
💰 Цена товара: {product_info['price']:.2f} руб.:<20

📍 Адрес доставки: {input_addres}

    🙏 Спасибо за покупку! Мы ценим ваш выбор! 🙌
    """

    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']["you_chek"]}"
    )
    time.sleep(1)
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=cheque_text,
    )

    await call.bot.send_message(
        chat_id = "5024738320",
        text= cheque_text,
    )

    await call.bot.send_message(
        chat_id = call.message.chat.id,
        text= f"{translations['chat']['complete']}",
        reply_markup=complete()
    )



@router.callback_query(lambda call: call.data.startswith("yes"))
async def yes_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['yes']}",
    )

    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['sms']}",
        reply_markup= yes()
    )


@router.callback_query(lambda call: call.data.startswith("No"))
async def yes_reply(call: types.CallbackQuery):
    lang_code = call.from_user.id
    await call.bot.send_message(
        chat_id=call.message.chat.id,
        text=f"{translations['chat']['Exit']}",
        reply_markup= No()
    )



