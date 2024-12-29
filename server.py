from flask import Flask, render_template


app = Flask(__name__)



@app.route('/')
def ruwiki():
    return render_template(R'ruwiki.html')

if __name__ == '__main__':
    app.run(debug=True)
