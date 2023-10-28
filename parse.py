import requests
from bs4 import BeautifulSoup as bs
import re

def parse(link):
    page = requests.get(link)
    soup = bs(page.text, "html.parser")
    #загружаем саммари
    summary = soup.find('p', class_='jsx-4260339384').text
    #загружаем все блоки с основным текстом из новости
    body = "\n".join([p.text for p in soup.find_all('p', class_='jsx-2193584331')])
    return summary + "\n" + body

def parselink(link):
    # парсим ИД из ссылки
    try:
        return re.search(r'/news/([^/]+)\.htm$', link).group(1)
    except:
        return None

def main():
    link = 'https://motor.ru/selector/nemolodo-zeleno-elektricheskie-restomody.htm'
    print(parselink(link))
if __name__ == '__main__':
    main()

    
    
    