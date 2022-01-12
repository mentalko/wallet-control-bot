from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


def main_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text="Сегодняшняя статистика", # /today
                ),
                KeyboardButton(
                    text="За текущий месяц", # /month
                )
            ],
            [
                KeyboardButton(
                    text="Последние расходы", # /expenses
                ),
                KeyboardButton(
                    text="Категории расходов", # /categories
                )
            ],
        ]
    )
    
def curency_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text="руб.",
                ),
                KeyboardButton(
                    text="грн.",
                ),
                KeyboardButton(
                    text="$",
                )
            ]
        ]
    )
