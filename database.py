from article import Article, User
import sqlite3
import hashlib


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
    def select(sql,params=()):
        connection = sqlite3.connect(Database.DB)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    
    def convert_to_articles(raw_articles):
        articles = []
        for id, title, content, photo in raw_articles:
            article = Article(title,content,photo,id)
            articles.append(article)
        return articles
    
    @staticmethod
    def create_table():
        with open (Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit
            connection.close

    @staticmethod
    def save(article: Article):
        if Database.find_article_by_title(article.title) is not None:
            return False
        Database.execute('INSERT INTO articles (title, content, photo)VALUES (?,?,?)', [article.title, article.content, article.photo])
        return True
    
    @staticmethod
    def find_article_by_id(id):
        articles = Database.convert_to_articles(Database.select('select * from articles where id = ?', [id]))
        if not articles:
            return None
        return articles[0]
    
    @staticmethod
    def delete_article_by_id(id):
        article = Database.find_article_by_id(id)
        if article is None:
            return False
        Database.execute('delete from articles where id = ?', [id])
        return True

    @staticmethod
    def update_article(id, title, content, photo):
        article = Database.find_article_by_id(id)
        if article is None:
            return False

        Database.execute("update articles set title = ?, content = ?, photo = ? where id = ?",[title,content,photo, id])
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

    @staticmethod
    def register_user(email, phone, password):
        password_hash = hashlib.md5(password.encode()).hexdigest()
        Database.execute("INSERT INTO users (email, phone, password_hash) VALUES (?,?,?)", [email,phone,password_hash])
        print(Database.select("SELECT * FROM users"))

    @staticmethod
    def can_be_logged_in(email_or_phone, password):
        user=Database.find_user_by_email_or_phone(email_or_phone)
        if user is None:
            return False
        password_hash = hashlib.md5(password.encode()).hexdigest()
        real_password_hash = Database.select('SELECT password_hash FROM users WHERE email = ? or phone = ?', [email_or_phone, email_or_phone])[0][0]

        if password_hash != real_password_hash:
            return False
        
        return True

    @staticmethod
    def find_user_by_email_or_phone(email_or_phone):
        print(email_or_phone)
        users=Database.select("SELECT * FROM users WHERE email = ? or phone = ?", [email_or_phone, email_or_phone])
        print(users)
        print(Database.select("SELECT * FROM users"))
        if not users:
            return None
        id, email, phone, password_hash = users[0]
        return User(email=email, phone=phone, id=id)