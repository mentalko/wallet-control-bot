from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сегодняшняя статистика", #: /today
                    callback_data='/today'
                ),
                InlineKeyboardButton(
                    text="За текущий месяц", #: /month
                    callback_data='/month'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Последние внесённые расходы", #: /expenses
                    callback_data='/expenses'
                ),
                InlineKeyboardButton(
                    text="Категории трат", #: /categories
                    callback_data='/categories'
                )
            ],
        ]
    )
    
def curency_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="руб.",
                    callback_data='_руб.'
                ),
                InlineKeyboardButton(
                    text="грн.",
                    callback_data='_грн.'
                ),
                InlineKeyboardButton(
                    text="$",
                    callback_data='_$'
                )
            ]
        ]
    )

def role_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Посмотреть ивенты",
                    callback_data='see'
                ),
                InlineKeyboardButton(
                    text="Создать ивент",
                    callback_data='create'
                )
            ]
        ]
    )

    # markup = InlineKeyboardMarkup()

    # markup.row(
    #     InlineKeyboardButton(
    #         text=f"Посмотреть ивенты",
    #         callback_data='see'
    #     ),
    #     InlineKeyboardButton(
    #         text="Создать ивент",
    #         callback_data='create'
    #     )
    # )
    # return markup