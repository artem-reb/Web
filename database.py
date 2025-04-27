from article import Article
import sqlite3


class Database:

    DB = 'database.db'
    SCHEMA = 'schema.sql'


    @staticmethod
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DB)
        cursor= connection.cursor()
        cursor.execute(sql,params)
        connection.commit()

    @staticmethod
    def create_table():
        with open (Database.SCHEMA) as schema_file:
            Database.execute(schema_file.read())

    @staticmethod
    def save(article: Article):
        if Database.find_article_by_title(article.title) is not None:
            return False
        Database.execute('INSERT INTO articles (title, content, photo)VALUES (?,?,?)', [article.title, article.content, article.photo])
        return True
    
    @staticmethod
    def get_all_articles():
        connection = sqlite3.connect(Database.DB)
        cursor= connection.cursor()
        cursor.execute("select * from articles ")
        raw_articles = cursor.fetchall()
        articles = []
        for id, title, content, photo in raw_articles:
            article = Article(title,content,photo,id)
            articles.append(article)
        print(articles)
        return articles
        
    
    @staticmethod
    def find_article_by_title(title):
        connection = sqlite3.connect(Database.DB)
        cursor= connection.cursor()
        cursor.execute("select * from articles where title = ?", [title])
        articles = cursor.fetchall()
        if len(articles) == 0:
            return None
        id, title, content, photo = articles[0]
        article = Article(title, content, photo, id)
        return article
