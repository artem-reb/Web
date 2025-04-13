from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from article import Article
from database import Database
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route('/', methods=["GET"])
@app.route('/index')
def index():
    return render_template('ruwiki.html')



database = {
    "sonic": {
        "title_article": "Ёж соник",
        "text_article": """
Соник — синий антропоморфный ёж, созданный художником Наото Осимой, программистом Юдзи Накой и дизайнером Хирокадзу Ясухарой. Во время разработки было предложено множество образов главного героя будущей игры, но разработчики остановились на ёжике синего цвета. Своё имя Соник получил за способность бегать на сверхзвуковых скоростях (англ. sonic — «звуковой; со скоростью звука»). Геймплей за Соника в большинстве игр серии Sonic the Hedgehog заключается в быстром прохождении уровней и битвах с врагами, для атаки которых Соник сворачивается в шар во время прыжка. Немаловажную роль для Соника играют золотые кольца, служащие ему в качестве защиты. Главным антагонистом героя является доктор Эггман, который хочет захватить мир и построить свою империю «Эггманленд».
""",
        "article_image_title": "Соник",
        "article_image_path": "sonic.png"
    },
    "naklz": {
        "title_article": "Наклз",
        "text_article": """
Наклз — красная антропоморфная ехидна, чьи иглы похожи на причёску из многочисленных коротких дредов. Можно заметить некоторое различие между игровым и неигровым спрайтами Наклза. В играх играбельный Наклз предстаёт в ярко-красном цвете с зелёными носками, а неиграбельный — как красно-розовый с жёлтыми носками. По официальным данным Наклзу 16 лет. День рождения, вероятно, 2 февраля — когда вышла первая игра с его участием — Sonic the Hedgehog 3, однако он может быть игровым персонажем в Sonic the Hedgehog 2 — достаточно лишь использовать картридж игры Sonic & Knuckles, в котором была задействована технология Lock-on. На его кулаках выделяются увеличенные костяшки пальцев (по 2 на каждой руке), отсюда и его имя (англ. knuckles — кастет). Он происходит из древнего клана ехидн, в котором также в своё время были вождь Пачакамак и Тикал. Упоминается, что Наклз — последний представитель своего клана.
""",
        "article_image_title": "Наклз",
        "article_image_path": "Knuckles06.png"
    },
    "breaking_bad" : {
        "title_article": "Во все тяжкие",
        "text_article": """
«Во все тя́жкие» (англ. Breaking Bad) — американская телевизионная криминальная драма, премьерные серии которой транслировались с 20 января 2008 года по 29 сентября 2013 года по кабельному каналу AMC. На протяжении пяти сезонов, состоящих из 62 эпизодов, показана история Уолтера Уайта, школьного учителя, у которого диагностировали неоперабельный рак лёгких. Вместе со своим бывшим учеником Джесси Пинкманом он начинает производить и продавать метамфетамин, чтобы обеспечить финансовое будущее своей семьи. Постановка и съёмка сериала велись в городе Альбукерке, штат Нью-Мексико.

Создатель и исполнительный продюсер сериала — Винс Гиллиган. Главные роли исполнили Брайан Крэнстон, сыгравший Уолтера Уайта, и Аарон Пол, ставший его сообщником Джесси Пинкманом. Анна Ганн стала Скайлер Уайт — женой Уолтера Уайта, Ар-Джей Митт — его сыном. Бетси Брандт исполнила роль сестры Скайлер — Мари Шрейдер, а её мужа Хэнка Шрейдера сыграл Дин Норрис. Во втором сезоне Уолтер нанял адвоката Сола Гудмана, в роли которого выступил Боб Оденкерк. Он в свою очередь познакомил Уолта с частным сыщиком Майком Эрмантраутом, сыгранным Джонатаном Бэнксом. Временным работодателем Уолта в сфере наркоторговли стал Густаво Фринг, в исполнении Джанкарло Эспозито. В заключительном сезоне сериала появились Джесси Племонс в роли Тода Алкиста, временного сообщника Уолтера Уайта, и Лора Фрейзер в роли Лидии Родарт-Куэйл, новой компаньонки Уолта.
""",
        "article_image_title": "Во все тяжкие",
        "article_image_path": "Breaking_Bad_logo.png"
    }
}

@app.route('/article/<name>')
def sonic_article(name):
    article= Database.find_article_by_title(name)
    if article is None:
        return f"<h1>Статьи '{name}' не существует!"
    return render_template('article.html', article=article)

@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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

    return redirect(url_for("show_articles"))

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