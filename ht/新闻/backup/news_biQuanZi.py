# -*- coding=utf-8  -*-
# @Time: 2020/7/27 15:13
# @Author: LeiLei Li
# @File: test.py

# import csv
#
# with open('test.csv', 'r', encoding='utf-8') as rf:
#     reader = csv.reader(rf, dialect=csv.excel)
#     for row in reader:
#         print('|'.join(row))



import requests
import time
import json
from bs4 import BeautifulSoup


import pymysql
import contextlib



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

    sql2 = """CREATE TABLE IF NOT EXISTS news_biQuanZi(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        title VARCHAR (100) ,
        content VARCHAR (5000),
        src_url VARCHAR (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=Myisam DEFAULT CHARSET=utf8;"""

    with mysql() as cursor:
        try:
            cursor.execute(sql2)
        except Exception as e:
            time.sleep(1)
            print(e)


def getNewsData():
    url = 'http://www.120btc.com/zixun/qukuai/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'text/html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    }

    html = requests.get(url, headers=headers, timeout=5)
    if html.status_code == 200:

        response = html.content.decode('utf-8')

        bs4 = BeautifulSoup(response, 'lxml')
        newsList = bs4.select('#showajaxnews > li')

        for newAll in reversed(newsList):
            img = newAll.find_all('img')[0].get('src')
            a = newAll.find_all('a')[0]
            title = a.get('title')
            href = a.get('href')
            newHref = 'http://www.120btc.com' + href

            res = requests.get(newHref, headers=headers, timeout=5)
            if res.status_code == 200:
                resp = res.content.decode('utf-8')
                soup = BeautifulSoup(resp, 'lxml')
                openTime = soup.select('div.page-time.text-ellipsis > span:nth-child(1)')[0].get_text()
                newsData = soup.select('div.main-box.article-main > div.page-content > p')

                # 获取正文

                detailNew = ''
                for detailsNew in newsData:
                    detailNew += detailsNew.get_text()
                    detailNew = str(detailNew) + str(r'\n')

                filter_list = ["开课", ]
                if any(filterName in detailNew for filterName in filter_list):
                    continue

                with mysql() as cursor:
                    sql = "insert into news_biQuanZi(time1, title, content,src_url)VALUES ('%s','%s','%s','%s')" % (
                        openTime, title, detailNew, img,)

                    try:
                        cursor.execute(sql)
                    except Exception as e:
                        time.sleep(1)
                        print(e)


if __name__ == '__main__':
    chuangjian()
    getNewsData()
