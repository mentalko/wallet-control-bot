import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram import types

from app.exceptions.NotCorrectMessage import NotCorrectMessage

import app.controllers.expense_controllers as expense_cnt
import app.controllers.user_controllers as user_cnt
import app.controllers.category_controllers as category_cnt

import app.utils.messages as messages 

from app.utils.config import WEBHOOK_HOST, WEBHOOK_PATH, DEVELOP

from app.db import check_db_exists
from app.keyboards.default import rk_menus


WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", '')
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID", '')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    if DEVELOP == 'False':
        logging.warning('Adding webhook...')
        await bot.set_webhook(WEBHOOK_URL)
        logging.warning('Done!')
    await check_db_exists()


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    if DEVELOP == 'False':
        logging.warning('Deleting webhook...')
        await bot.delete_webhook()
        logging.warning('Done!')

    logging.warning('Bye!')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
        Sending welcome message to user
    """
    if not await user_cnt.user_is_exists(message.from_user.id):
        await user_cnt.add_new_user(message.from_user, currency=None)
        await message.answer( messages.WELCOM_MSG, reply_markup=rk_menus.curency_keyboard())
    else:
        await bot.send_message(message.from_user.id, messages.HELP_MSG, reply_markup=rk_menus.main_keyboard())
        

@dp.message_handler(lambda message: message.text in ["руб.", "грн.", "$"]) 
async def get_curency(message: types.Message,):
    """
        Sending help message to user
    """
    code = message.text
    await user_cnt.add_new_user(message.from_user, currency=code)
    await send_welcome(message)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
        Sending help message to user
    """
    await message.answer(messages.HELP_MSG)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = message.text[4:]
    await expense_cnt.delete_expense(row_id)

    answer_message = "Удалил ✔️"
    await message.answer(answer_message)
    
@dp.message_handler(text='Категории расходов') 
@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """
        Sending category list
    """
    answer_message = await category_cnt.get_categories_list()
    # await message.answer(await category_cnt.get_categories_list())
    await message.answer(answer_message)

@dp.message_handler(text='Сегодняшняя статистика') 
@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """
        Sending statistics today
    """
    answer_message = await expense_cnt.get_today_statistics(message.from_user.id)
    await message.answer(answer_message)


@dp.message_handler(text='За текущий месяц') 
@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """
        Sending statistics for the current month
    """
    answer_message = await expense_cnt.get_month_statistics(message.from_user.id)
    await message.answer(answer_message)

@dp.message_handler(text='Последние расходы') 
@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = await expense_cnt.last(message.from_user.id)
    currency_name = await user_cnt.get_curency_name(message.from_user.id)

    if not last_expenses:
        await message.answer("Расходы ещё не заведены❗")
        return

    last_expenses_rows = [
        f"{expense['amount']} {currency_name} на {expense['category_name']} — нажми "
        f"/del{expense['id']} для удаления"
        for expense in last_expenses]

    answer_message = "Последние сохранённые траты:\n\n🔸 " + "\n\n🔸 "\
            .join(last_expenses_rows)

    await message.answer(answer_message)



@dp.message_handler(lambda message: message.text.startswith('/set_budget'))
async def set_budget(message: types.Message):
    """
        Setting budget limit
    """
    currency_name = await user_cnt.get_curency_name(message.from_user.id)

    try:
        budget = await user_cnt.set_budget(message.from_user.id, message.text)
        await message.answer(f"Установлен бюджет в размере {budget} {currency_name} ✔️")
    except NotCorrectMessage as e:
        await message.answer(str(e))

@dp.message_handler()
async def add_expense(message: types.Message):
    """
        Adding new expense
    """
    user_id = message.from_user.id
    
    currency_name = await user_cnt.get_curency_name(user_id)
    

    try:
        expense = await expense_cnt.add_expense(user_id, message.text)
    except NotCorrectMessage as e:
        await message.answer(str(e))
        return

    answer_message = (
        f"Добавлены траты {expense['amount']} {currency_name} на {expense['category_name']} ✔️\n\n"
        f"{await expense_cnt.get_today_statistics(user_id)}")

    await message.answer(answer_message)
