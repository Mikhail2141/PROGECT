from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_menu():
    keyboard = [
        [InlineKeyboardButton(text="✉️ Отправить артикул", callback_data="artikul")],
        [InlineKeyboardButton(text="💬 Задать вопрос", callback_data="ask")],
        [InlineKeyboardButton(text="➡️ Телеграм канал", url="https://t.me/mp_techno")],
        [InlineKeyboardButton(text="❗ FAQ", callback_data="faq")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



def buy():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🛒 Указать адрес доставки и купить товар", callback_data="Buy")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def meneger():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="❓ Задать вопрос", url = "https://t.me/kazantipooo")]),
    keyboard.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="start_menu")]),
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def dostavka():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🚴‍♂️ Курьер", callback_data="courier")]),
    keyboard.append([InlineKeyboardButton(text="🏠 ПВЗ", callback_data="pvz")]),
    keyboard.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="start_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def PVZ():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🟢 Выбрать ПВЗ", url="https://www.cdek.ru/ru/offices/")]),
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="Buy")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="start_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cheque():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text= "🧾 Сформировать чек" , callback_data="chek")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_buy():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="Buy")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def F_menu():
    keyboard =[]
    keyboard.append([InlineKeyboardButton(text="О доставке и оплате", callback_data="DB")]),
    keyboard.append([InlineKeyboardButton(text="О возвратах и обмене", callback_data="VO")]),
    keyboard.append([InlineKeyboardButton(text="О консультациях", callback_data="K")]),
    keyboard.append([InlineKeyboardButton(text="О работе канала", callback_data="RK")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def complete():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="🟢 Да", callback_data="yes")]),
    keyboard.append([InlineKeyboardButton(text="🔴 Нет", callback_data="No")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



def yes():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="➡️ Перейти в чат с менеджером", url = "https://t.me/kazantipooo")]),
    keyboard.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="start_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def No():
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="➡️ Наш магазин", url="https://t.me/mp_techno")]) ,
    keyboard.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="start_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)