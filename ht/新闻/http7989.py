# -*- coding = utf-8  -*-
# @Time: 2020/5/8 17:28
# @Author: 李雷雷
# @File: http7989.py

import json
import pymysql
import logging

# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request


# 实例化，可视为固定格式
app = Flask(__name__)
# route()方法用于设定路由；类似spring路由配置


#从数据库中查询具体id的那一条数据
@app.route('/python/xinwen/size=<string:size>')
def meilin_page(size):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

        # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='huihuang', charset='utf8')
        cursor = conn.cursor()

        if size == 0 or size == 1:
            size = 1
        sql = "select * from qm_information ORDER BY id DESC LIMIT " + str(size)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':str(a[i][0]),'addtime': str(a[i][1]),'title': str(a[i][2]), 'content': str(a[i][3])}

            # dict['id'] = str(a[i][0])
            # dict['addtime'] = a[i][1]
            # dict['title'] = str(a[i][2])
            # dict['content'] = str(a[i][3])
            L.append(dict)
        L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(host='0.0.0.0',port=7989, debug=True,)
