import sqlite3

class Database:
    def __init__(self):
        self.database = sqlite3.connect('parser.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)  #  args - кортеж бесконечных элементов
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(30) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def save_category(self, category_title):
        sql = '''
        INSERT INTO categories(category_title) VALUES (?)
        ON CONFLICT DO NOTHING
        '''
        self.manager(sql, category_title, commit=True)

    def get_category_id(self, category_title):
        sql = '''
        SELECT category_id FROM categories WHERE category_title = ?
        '''
        return self.manager(sql, category_title, fetchone=True)

    def create_articles_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS articles(
            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_title TEXT UNIQUE,
            article_link TEXT,
            article_intro TEXT,
            article_image TEXT,
            article_date TEXT
        )
        '''
        self.manager(sql, commit=True)

    def save_article(self, article_title, article_link,article_intro,article_image,article_date):
        sql = '''INSERT INTO articles(article_title, article_link, article_intro,
                     article_image, article_date) VALUES (?,?,?,?,?)
                     ON CONFLICT DO NOTHING
                     '''
        self.manager(sql, article_title, article_link, article_intro, article_image, article_date,
                      commit=True)
