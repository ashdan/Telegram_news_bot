from httpx import AsyncClient
import feedparser
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#Тут подгружаем процедуры из наших модулей
from parse import parselink
from sql import create_table, save_to_db, select_for_db
from entrails.keyboard import first_collection
from entrails import handlers

#Подгружаем переменные
from variables import BOT_TOKEN, CHAT_ID

#Подключаем бота
bot = Bot(token=BOT_TOKEN)

async def feed_reader():
    rss_link = 'https://motor.ru/exports/rss'
    
    #создаем экземпляр класса AsyncClient() и посылаем асинхронный get 
    httpx_client = AsyncClient()
    rss_text = await httpx_client.get(rss_link)
    #Парсим RSS ленту
    rss = feedparser.parse(rss_text.text)
    
    for news in rss.entries[::-1]:
        news_id = parselink(news['link'])
        #Если ссылка именно на новость, а не на другой раздел сайта
        if news_id is not None:
            #Если записи нет в базе данных:
            if await select_for_db(news_id, 'news_id') is None:
                #Сохраняем запись в БД:
                await save_to_db(news_id, news['title'], news['link'])
                
                await send_message_to_bot(f'<b>{news["title"]}</b>\n{news["summary"]}\n<a href="{news["link"]}">Link</a>')

                # - спим 4 секунды, можно больше после каждой итерации с новой записью.
                await asyncio.sleep(4)
            else:
                #Если запись уже есть - пропускаем
                continue

async def send_message_to_bot(text):
    await bot.send_message(chat_id=CHAT_ID,
                           text=text,
                           parse_mode='HTML',
                           reply_markup=first_collection())

async def main():
    #Не забываем про диспетчера и удаляем webhook на всякий случай
    dp = Dispatcher()
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)

    #создаем БД, есои ее нет
    await create_table()

    #вызываем чтение ленты
    await feed_reader()
    
    #создаем экземпляр класса AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    #создаем задачу в режиме 'cron' которая будет запускать процедуру feed_reader() в 10:30 и 17:30
    scheduler.add_job(feed_reader, 'cron', hour='10,17', minute='30')
    #стартуем работу
    scheduler.start()

    #пуллим бот - чтобы наш скрипт постоянно запрашивал сервер ТГ о состоянии нашего бота
    await dp.start_polling(bot)
        
if __name__ == '__main__':
    asyncio.run(main())
