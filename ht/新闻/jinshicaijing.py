# -*- coding=utf-8  -*-
# @Time: 2020/6/19 10:58
# @Author: LeiLei Li
# @File: jinshicaijing.py



import requests
import json
from datetime import datetime
import time
import pymysql
import contextlib
from utils import get_html,get_html_bytes

@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='BXrXpK7Z7dSEK9lK',db='sj', charset='utf8'):
# def mysql(host='localhost', port=3306, user='root', passwd='123456',db='lll', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 生成游标对象
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def chuangjian():

    with mysql() as cursor:
        sql2 = """CREATE TABLE IF NOT EXISTS jscj(
                id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
                time1 VARCHAR(50) ,
                content VARCHAR (300),
                UNIQUE KEY `content` (`content`))  ENGINE=MyISAM DEFAULT CHARSET=utf8;"""
        cursor.execute(sql2)
        print('创建成功！')


def getdata():
    url = 'https://www.jin10.com/flash_newest.js'
    html = get_html(url)
    # res = html.text

    # js对象，截取json字符串，并转化为json格式
    res = json.loads(html[13:-1])
    res = res[0:10]
    for data in reversed(res):
        content = data.get('data').get('content')
        remark = data.get('remark')

        # 过滤掉带链接的
        if content and 'a' in content:
            time.sleep(1)
            continue
        # 过滤掉内容是图片超链接
        if remark and data.get('data').get('pic'):
            time.sleep(1)
            continue

        time1 = data.get('id')
        if time1 and content:
            hour = time1[8:10]
            minute = time1[10:12]
            second = time1[12:14]
            timeArray = hour+':'+minute+':'+second

            filter_list = ["图示", ]
            if any(filterName in content for filterName in filter_list):
                continue

            with mysql() as cursor:
                sql = "insert into jscj(time1, content)values('%s','%s')" % (timeArray, content)
                try:
                    cursor.execute(sql)
                except Exception as e:
                    time.sleep(2)
                    print(e)

            # print(timeArray, (content))
    # time.sleep(10)
        
if __name__ == '__main__':
    # chuangjian()
    getdata()