import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql
from flaskr.db import init_db, DBManager

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        db = DBManager()
        cursor = db.db_cursor()
        article = {
            'title': request.form['artTitle'].replace("'", "\""),
            'resource': request.form['orir'],
            'html': request.form['artHtml'].replace("'", "\""),
            'content': request.form['artContent'].replace("'", "\"")
        }
        sql_string = f"INSERT INTO `article` (`artTitle`, `artHtml`, `artContent`,  `artResource`) VALUES ('{article['title']}','{article['html']}','{article['content']}' ,'{article['resource']}' )"
        try:
            print(123)
            cursor.execute(sql_string)
            db.db_commit()
        except pymysql.Error as e:
            print(e.args[0], e.args[1])
            db.db_rollback()
        cursor.close()
        return redirect(url_for('index'))
    else:
        return render_template('admin/editor.html')
