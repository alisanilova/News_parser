# Импортируем библиотеки
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from user_agent import generate_user_agent

# Генерируем случайного пользовательского агента, чтобы не заблокировали
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux', 'win'))}

# Основная функция программы - создает новостную подборку по ключевым словам в интересущем источнике
def get_news(source, keywords):
    news_digest = []
    for page in range(1, 30):  # Задаем диапапзон прокрутки страниц в ленте новостей
        url = source + "search?query=&page=" + str(page)
        response = requests.get(url, timeout=5, headers=headers)  # Выполняем запрос к сайту
        soup = bs(response.text, "lxml")  # Извлекаем "сырой" код html
        news_names = soup.find_all("a", class_="b-inline-article__preview")  # Ищем в коде разметки заголовки новостей

        # Перебираем заголовки новостей и проверяем есть ли хотя бы одно из ключевых слов в заголовке
        for name in news_names:
            keys_in_news = []
            for keyword in keywords:
                if keyword in name.text.lower():
                    news_attributes = []
                    keys_in_news.append(keyword)

                    # Исключаем дублирование новостей, если в новости присутствует несколько ключевых слов
                    if name.text.strip() in [news_digest[i][0] for i in range(len(news_digest))]:
                        continue
                    # По каждой тематической новости создаем список, включающий заголовок, ссылку, дату и список ключевых слов
                    else:
                        news_attributes.append(name.text.strip())
                        link = 'https://www.dp.ru/' + name["href"]
                        news_attributes.append(link)
                        date = re.findall(r'\d{4}/\d{2}/\d{2}', link)
                        date = date[0][-2:] + date[0][-3] + date[0][-5:-2] + date[0][-10:-6]
                        news_attributes.append(date)
                    news_digest.append(news_attributes)
                    news_digest[-1].append(keys_in_news)
    return news_digest

source = "https://www.dp.ru/"
keywords = ["сетл", "setl", "лср", "ленспецсму","строит", "строй", "недвижимост", "девелоп", "ипотек", "жилищ"]

# Формируем таблицу
df = pd.DataFrame(data=get_news(source, keywords), columns=["Заголовок", "Ссылка", "Дата", "Ключевые слова"])
df.index = range(1, len(df) + 1)

# Отправляем результат в файл
file_name = "Новости.csv"
df.to_csv(file_name, encoding="utf-16", sep="|")

print("Завершено успешно")

# Попытка отправить результат по почте. Работала криво, меня заблокировали за подозрение на спам, оставила в коде для разбора
#import smtplib
#smtp_obj = smtplib.SMTP('smtp.yandex.ru', 587)
#smtp_obj.starttls()
#smtp_obj.login("email1@yandex.ru",'password')
#smtp_obj.sendmail("email1@yandex.ru", "email2@gmail.com", df)
#smtp_obj.quit()




