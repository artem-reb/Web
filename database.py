from article import Article


class Database:
    articles = []


    @staticmethod
    def save(article: Article):
        Database.articles.append(article)
    
    def get_all_articles():
        return Database.articles
    
    def find_article_by_title(title):
        for article in Database.articles:
            if article.title == title:
                return article 
            return None 