#SQL requests

import aiosqlite

#Создаем БД, если ее нет в каталоге
async def create_table():
    async with aiosqlite.connect('storage.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS motor '
                         '(id integer, news_id text, title text, link text, status text, date text, PRIMARY KEY(id AUTOINCREMENT))')
        await db.commit()

#Создаем запись с новостью, заголовком и ссылкой
async def save_to_db(news_id, title, link):
    async with aiosqlite.connect('storage.db') as db:
        await db.execute('INSERT INTO motor (news_id, title, link) VALUES (?, ?, ?)',
                         (news_id, title, link))
        await db.commit()

#Обновляем запись в БД по ИД
async def update_db(news_id, status, date):
    async with aiosqlite.connect('storage.db') as db:
        await db.execute('UPDATE motor SET status = ?, date = ? WHERE news_id = ?',
                         (status, date, news_id))
        await db.commit()

#Запрашиваем данные
async def select_for_db(news_id, column):
    async with aiosqlite.connect('storage.db') as db:
        cursor = await db.cursor()
        await cursor.execute(f'SELECT {column} FROM motor WHERE news_id = ?',(news_id,))
        return await cursor.fetchone()