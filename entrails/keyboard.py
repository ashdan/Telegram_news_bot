#keyboards collection
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def first_collection() -> InlineKeyboardMarkup:
    #Отправка в ChatGPT
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Send to Chat-GPT', callback_data='gpt_button_pressed')
    buttons.button(text='Delete', callback_data='gpt_button_delete')
    buttons.adjust(2)
    return buttons.as_markup()

def second_collection() -> InlineKeyboardMarkup:
    #Отправка в канал
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Send to Channel', callback_data='channel_button_pressed')
    buttons.adjust(1)
    return buttons.as_markup()