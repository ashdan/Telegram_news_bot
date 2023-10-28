from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
import datetime

#импортируем переменные
from variables import CHAT_ID, CHANNEL_ID

#импортируем процедуру работы с БД
from sql import update_db, select_for_db
#импортируем парсер новости и парсер ссылки
from parse import parse, parselink
#импортируем вторую коллекцию кнопок
from entrails.keyboard import second_collection
#импортируем процедуру работы с ChatGPT
from gptai import get_GPT
#импортируем процедуру feed_reader()
from bot import feed_reader


#подключаем роутер
router = Router()

#если новость не нужна - удаляем
@router.callback_query(F.data=='gpt_button_delete')
async def delete_message(callback: CallbackQuery):
    try:
        await callback._bot.delete_message(chat_id=CHAT_ID, message_id=callback.message.message_id)
        for item in callback.message.entities:
            if item.type == 'text_link': 
                post = item.url
        id = parselink(post)
        await update_db(id,'Del', datetime.datetime.now())
    except:
        for item in callback.message.entities:
            if item.type == 'text_link': 
                post = item.url
        id = parselink(post)
        await update_db(id,"Can't del - more 48H", datetime.datetime.now())

#Отправляем новость на съедение ChatGPT
@router.callback_query(F.data=='gpt_button_pressed')
async def get_link(callback: CallbackQuery):
    for item in callback.message.entities:
         if item.type == 'text_link': 
            post = item.url#url на новость
            id = parselink(post)#получаем из url id-новости
            text =  parse(post)#чистый текст новости
            title = await select_for_db(id, 'title')#берем заголовок из базы
            brief = get_GPT(text)#получает текст от ChatGpt
            
            #формируем текст сообщения     
            format_text = f'<b>{title[0]}</b>\n{brief}\n<a href="{post}">Link</a>'
            
            #добавляем в базу статус и время отправки сообщения
            await update_db(id,'Send', datetime.datetime.now())
            #отправляем сообщение
            await callback.message.answer(format_text,
                                            parse_mode='HTML',
                                            disable_web_page_preview=True,
                                            reply_markup=second_collection())
    #пробуем удалить исходное сообщение
    try:
        await callback._bot.delete_message(chat_id=CHAT_ID, message_id=callback.message.message_id)
    except:
        print(f"{callback.message.message_id} can't be deleted")

# Отправляем сообщение в канал, без кнопки
@router.callback_query(F.data=='channel_button_pressed')
async def send_tochat(callback: CallbackQuery):
    await callback._bot.copy_message(chat_id=CHANNEL_ID, 
                                     from_chat_id=CHAT_ID, 
                                     message_id=callback.message.message_id)
    try:
        await callback._bot.delete_message(chat_id=CHAT_ID, 
                                       message_id=callback.message.message_id)
    except:
        print(f"{callback.message.message_id} can't be deleted")

@router.message (Command(commands=['start', 'load']))
async def load_news(message: Message):
    await feed_reader()