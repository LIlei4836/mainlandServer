# -*- coding = utf-8  -*-
# @Time: 2020/7/1 11:20
# @Author: 李雷雷
# @File: http7988.py

# 金十财经咨询（去除图片，超链接）

import json
import pymysql
import logging

# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS


# 实例化，可视为固定格式
app = Flask(__name__)
# route()方法用于设定路由；类似spring路由配置
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/python/jscj/size=<string:size>')
def jscj_size(size):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()

        if size == 0 or size == 1:
            size = 1
        sql = "select * from jscj ORDER BY id DESC LIMIT " + str(size)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':str(a[i][0]),'time': str(a[i][1]),'content': str(a[i][2]),}

            # dict['id'] = str(a[i][0])
            # dict['addtime'] = a[i][1]
            # dict['title'] = str(a[i][2])
            # dict['content'] = str(a[i][3])
            L.append(dict)
        L = jsonify(L)
        # L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        print(e)

@app.route('/python/jscj/page=<int:page>')
def jscj_page(page):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()


        if page == 0 or page == 1:
            page = 1
        sql = "select * from jscj ORDER BY id DESC LIMIT " + str(int((20 * page)-20)) + ','+ str(20)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':a[i][0],'time': a[i][1],'content': a[i][2], }
            L.append(dict)
        L = jsonify(L)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)


@app.route('/python/edcj/size=<string:size>')
def edcj_size(size):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()

        if size == 0 or size == 1:
            size = 1
        sql = "select * from news_erDuoCaiJing ORDER BY id DESC LIMIT " + str(size)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':str(a[i][0]),'time': str(a[i][1]),'title': str(a[i][2]), 'content':a[i][3],'src':a[i][4], 'img':a[i][5]}
            L.append(dict)
        L = jsonify(L)
        # L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        print(e)

@app.route('/python/edcj/page=<int:page>')
def edcj_page(page):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()


        if page == 0 or page == 1:
            page = 1
        sql = "select * from news_erDuoCaiJing ORDER BY id DESC LIMIT " + str(int((20 * page)-20)) + ','+ str(20)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id': str(a[i][0]), 'time': str(a[i][1]), 'title': str(a[i][2]), 'content': a[i][3], 'src': a[i][4] ,'img':a[i][5]}
            L.append(dict)
        L = jsonify(L)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)


@app.route('/python/qscm/size=<string:size>')
def qscm_size(size):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()

        if size == 0 or size == 1:
            size = 1
        sql = "select * from news_quShiChuanMei ORDER BY id DESC LIMIT " + str(size)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':str(a[i][0]),'time': str(a[i][1]),'title': str(a[i][2]), 'content':a[i][3],'src':a[i][4], 'img':a[i][5]}
            L.append(dict)
        L = jsonify(L)
        # L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        print(e)

@app.route('/python/qscm/page=<int:page>')
def qscm_page(page):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()


        if page == 0 or page == 1:
            page = 1
        sql = "select * from news_quShiChuanMei ORDER BY id DESC LIMIT " + str(int((20 * page)-20)) + ','+ str(20)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id': str(a[i][0]), 'time': str(a[i][1]), 'title': str(a[i][2]), 'content': a[i][3], 'src': a[i][4] ,'img':a[i][5]}
            L.append(dict)
        L = jsonify(L)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)


@app.route('/python/hxcj/size=<string:size>')
def hxcj_size(size):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()

        if size == 0 or size == 1:
            size = 1
        sql = "select * from news_huoXingCaiJing ORDER BY id DESC LIMIT " + str(size)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':str(a[i][0]),'time': str(a[i][2]),'title': str(a[i][3]), 'content':a[i][4],'src':a[i][5],}
            L.append(dict)
        L = jsonify(L)
        # L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        print(e)

@app.route('/python/hxcj/page=<int:page>')
def hxcj_page(page):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        cursor = conn.cursor()


        if page == 0 or page == 1:
            page = 1
        sql = "select * from news_huoXingCaiJing ORDER BY id DESC LIMIT " + str(int((20 * page)-20)) + ','+ str(20)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id': str(a[i][0]), 'time': str(a[i][2]), 'title': str(a[i][3]), 'content': a[i][4],
                    'src': a[i][5], }
            L.append(dict)
        L = jsonify(L)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(host='0.0.0.0',port=7988,debug=True)
