from article import Article
import sqlite3


class Database:
    articles = []

    DB = 'database.db'
    SCHEMA = 'schema.sql'


    @staticmethod
    def execute(sql, params):
        connection = sqlite3.connect(Database.DATABASE)
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
        Database.execute('INSERT INTO articles VALUES (?,?,?)', [article.title, article.content, article.photo])
        return True
    
    @staticmethod
    def get_all_articles():
        return Database.articles
    
    @staticmethod
    def find_article_by_title(title):
        connection = sqlite3.connect(Database.DATABASE)
        cursor= connection.cursor()
        cursor.execute("select * from articles where title = ?", [title])
        articles = cursor.fetchall()
        if len(articles) == 0:
            return None
        article = Article(articles[0][0], 
                          articles[0][1], 
                          articles[0][2],
                          articles[0][3]
                          )
        return articles[0]
