from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from article import Article
from database import Database
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


Database.create_table()

@app.route('/', methods=["GET"])
@app.route('/index')
def index():
    articles = Database.get_all_articles()
    groups = []
    k = 3
    for i in range(0, len(articles), k):
        groups.append(articles[i:i+k])
    return render_template("ruwiki.html", groups=groups)


@app.route('/article/<name>')
def sonic_article(name):
    article= Database.find_article_by_title(name)
    if article is None:
        return f"<h1>Статьи '{name}' не существует!"
    return render_template('sonic_article.html', article=article)

@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_article/<int:id>', methods=['POST'])
def delete_article(id):
    deleted = Database.delete_article_by_id(id)
    if not deleted:
        abort(404, f"Article with id '{id}' doesn't exist")
    return redirect(url_for('index'))

@app.route("/add_article", methods=['GET', 'POST'])
def add_article():
    if request.method == "GET":
        return render_template('add_article.html')
    
    title = request.form["title"]
    if title is None:
        flash("Для статьи необходимо указать название")
        redirect(request.url)
        return
    
    content = request.form["content"]
    if content is None:
        flash("Для статьи необходимо указать текст")
        redirect(request.url)
        return
    
    photo = request.files["photo"]
    if photo is None or photo.filename is None:
        flash("Для статьи необходимо указать фото")
        redirect(request.url)
        return
    photo.save(app.config["UPLOAD_FOLDER"] + photo.filename)

    article = Article(title, content, photo.filename)
    Database.save(article)

    return redirect(url_for("index"))

@app.route('/articles')
def show_articles():
    articles = Database.get_all_articles()
    groups = []
    k = 3
    for i in range(0, len(articles), k):
        groups.append(articles[i:i+k])

    return render_template('articles.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True)