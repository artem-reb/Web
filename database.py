from article import Article


class Database:
    articles = []


    @staticmethod
    def save(article: Article):
        Database.articles.append(article)
    
    def get_all_articles():
        return Database.articles
    