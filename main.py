import requests
from bs4 import BeautifulSoup
from Database import Database


db = Database()
db.create_categories_table()
db.create_articles_table()

html = requests.get('https://www.gazeta.ru/').text
soup = BeautifulSoup(html, 'html.parser')
categories_block = soup.find('div',class_='b_main')
categories = categories_block.find_all('a',class_="b_ear")

for category in categories:
     print(category)
     categories_text = category.get_text(strip=True)
     db.save_category(categories_text)
     categories_url = 'https://www.gazeta.ru' + category.get('href')
     article_html = requests.get(categories_url).text
     article_soup = BeautifulSoup(article_html,'html.parser')
     article_block = article_soup.find_all('article', class_='b_article')

     for article in article_block:
         time = article.find('time', class_='time').get_text(strip=True)
         article_img = article.find('img').get('data-hq')
         if article_img == None:
             article_img = article.find('img').get('src')
         else:
             article_img = article.find('img').get('data-hq')
         article_info = article.find('div', class_='b_article-text').get_text(strip=True)
         db.save_article(categories_text, categories_url, article_info, article_img, time)