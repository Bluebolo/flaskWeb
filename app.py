import os.path

from flask import Flask, render_template, request, abort
from flaskr.db import init_db
import markdown,codecs

app = Flask(__name__)

from flaskr.bluePrint.auth import bp as auth_bp
from flaskr.bluePrint.api import bp as api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index():  # put application's code here
    return render_template('introduction/index.html')


@app.route('/about')
def about():
    return render_template('introduction/about.html')


@app.route('/archives')
def archives():
    return render_template('introduction/archives.html')


@app.route('/links')
def links():
    return render_template('introduction/links.html')


@app.route('/read')
def read():
    # with app.open_resource('static/markdown/百度.md') as f:
    #     text = f.read()
    # print(os.listdir('./static/markdown'))
    # return text
    return render_template('read/read_list.html')


@app.route('/read/<title>')
def read_md(title=None):
    input_file = codecs.open('./static/markdown/' + title, mode="r", encoding="utf-8")
    # f = open('./static/markdown/' + title, encoding='utf-8')
    text = input_file.read()
    html = text
    title = title[:-3]
    # with app.open_resource('static/markdown/' + title) as f:
    #     text = f.read()
    #     text.
    #     print(text)
    return render_template('read/read_single.html', title=title, text=html)

@app.route('/article/id/<art_id>')
def article_id(art_id=None):
    cursor = init_db()
    first = cursor.execute(
        f'SELECT `artId`,`artTitle`, `artHtml`, `artTime`, `show` FROM `article` WHERE `artId` = {art_id}   LIMIT 1 OFFSET 0')
    art_data = {}
    if first == 1:
        contain = cursor.fetchone()
        art_data = {
            'artTitle': contain[1],
            'artHtml': contain[2],
            'artTime': contain[3]
        }
    else:
        abort(404)
    return render_template('article/essay.html', data=art_data)




if __name__ == '__main__':
    app.run()
