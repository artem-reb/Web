from flask import Flask, render_template


app = Flask(__name__)



@app.route('/')
def ruwiki():
    return render_template('ruwiki.html')


@app.route('/hello')
def hello():
    return '<h1>Hello, World!<h1>'


@app.route('/sonic')
def sonic_article():
    title_article = "Ёж Соник"
    text_article = """
Соник — синий антропоморфный ёж, созданный художником Наото Осимой, программистом Юдзи Накой и дизайнером Хирокадзу Ясухарой. Во время разработки было предложено множество образов главного героя будущей игры, но разработчики остановились на ёжике синего цвета. Своё имя Соник получил за способность бегать на сверхзвуковых скоростях (англ. sonic — «звуковой; со скоростью звука»). Геймплей за Соника в большинстве игр серии Sonic the Hedgehog заключается в быстром прохождении уровней и битвах с врагами, для атаки которых Соник сворачивается в шар во время прыжка. Немаловажную роль для Соника играют золотые кольца, служащие ему в качестве защиты. Главным антагонистом героя является доктор Эггман, который хочет захватить мир и построить свою империю «Эггманленд».
"""
    article_image_title = "Соник"
    article_image_path = "static/sonic.png"
    return render_template('sonic_article.html', title_article=title_article, article_image_title=article_image_title, text_article=text_article, article_image_path=article_image_path)

@app.route('/base')
def base():
    return render_template('base.html', title='Китайский новый год')


@app.route('/max')
def find_max():
    a = int(request.args['a'])
    b = int(request.args['b'])

    if a > b:
        return f'<h1>The maximum number is {a}<h1>'
    else:
        return f'<h1>The maximum number is {b}<h1>'



if __name__ == '__main__':
    app.run(debug=True)
