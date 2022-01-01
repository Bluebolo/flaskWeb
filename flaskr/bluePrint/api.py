import functools
import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import init_db
import time
import datetime

bp = Blueprint('api', __name__, url_prefix='/api')


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


# 获得文章标题列表
@bp.route('/get/article')
def get_article():
    nums = request.args.get('nums', '')
    if nums == '':
        nums = 20
    print(nums)
    cursor = init_db()
    _sql = f"SELECT `artId`, `artTitle`, `artTime` FROM `article` WHERE `show` = 'yes' ORDER BY `artId` DESC LIMIT {nums} OFFSET 0 "
    cursor.execute(_sql)
    result = cursor.fetchall()
    cursor.close()
    data = {
        'arc': []
    }
    for item in result:
        data['arc'].append({
            'artId': item[0],
            'artTitle': item[1],
            'artTime': item[2].strftime("%Y-%m-%d %H:%M:%S")
        })
    return data


@bp.route('/get/md')
def get_md():
    file_list = os.listdir('./static/markdown')
    data = {
        'md': []
    }
    for item in file_list:
        data['md'].append({
            'title': item,
            'change_time': TimeStampToTime(os.path.getctime('./static/markdown/' + item)),
            'create_time': TimeStampToTime(os.path.getmtime('./static/markdown/' + item))
        })
    return data
