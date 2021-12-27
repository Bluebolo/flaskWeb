# 基本设置
import os.path

from flask import Flask, render_template, request, abort
from flaskr.db import init_db

app = Flask(__name__)

# flaskr.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Dcsj0519_@sh-cynosdbmysql-grp-daa9yhas.sql.tencentcdb.com:27796/blog'
# flaskr.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(flaskr)

# class Tags(db.Model):
#     __tablename__ = 'tags'
#     id = db.Column(db.Integer, primary_key=True)
#     tagInfo = db.Column(db.String(64))
#     articleId = db.Column(db.String(64))
#
#     def __repr__(self):
#         return 'Role:%s'% self.tagInfo
from flaskr.bluePrint.auth import bp as auth_bp
from flaskr.bluePrint.api import bp as api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

from flaskr.db import init_db


# 主页
@app.route('/')
def index():
    return render_template('index.html')


# 索引
@app.route('/archives')
def archives():
    return render_template('archives.html')


# 关于
@app.route('/about')
def about():
    return render_template('about.html')


# 友链
@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/read')
def read():
    # with app.open_resource('static/markdown/百度.md') as f:
    #     text = f.read()
    # print(os.listdir('./static/markdown'))
    # return text
    return render_template('read_list.html')


import markdown
@app.route('/read/<title>')
def read_md(title=None):
    f = open('./static/markdown/' + title,encoding='utf-8')
    text = f.read()
    text = markdown.markdown(text)
    print(text)
    # with app.open_resource('static/markdown/' + title) as f:
    #     text = f.read()
    #     text.
    #     print(text)
    return render_template('read_content.html',title=title,text=text)


# 文章
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
    return render_template('article.html', data=art_data)
