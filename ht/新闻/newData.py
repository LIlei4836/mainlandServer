# -*- coding=utf-8  -*-
# @Time: 2020/7/8 9:47
# @Author: LeiLei Li
# @File: newData.py

import requests
import json
import time
from bs4 import BeautifulSoup
from utils import get_html_bytes,get_html

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



def getData():
    url = 'https://www.fx112.com/bitcoin/'
    res = get_html(url)
    soup = BeautifulSoup(res, 'lxml')
    newsLists = soup.select('#centerdiv > div.conleft > div.artlist > div.artcon > div')
    for news in reversed(newsLists):
        imgs = news.img['src']
        oldhref = news.a['href']
        href = 'https://www.fx112.com' + oldhref
        title = news.select('h3 a')[0].get_text()

        resp = get_html(href)
        newSoup = BeautifulSoup(resp, 'lxml')
        stringTime = newSoup.select('div.conleft > div.artinfo > span:nth-child(1)')[0].get_text()
        timeStamp = '发布日期：' + stringTime[:16]

        # 正文
        detailNews = newSoup.select('.article p')[:-1]
        detailNew = ''
        for detailsNew in detailNews:
            detailNew += detailsNew.get_text()
            detailNew = str(detailNew) + str(r'\n')

        filter_list = ["太壹科技", "哼哈互动", "优盾", "金色"]

        if any(filterName in detailNew for filterName in filter_list):
            print(title)
            continue

        if any(filterName in title for filterName in filter_list):
            continue

        with mysql() as cursor:
            sql = "insert into hz_ada(time1,title,content,src_url)VALUES ('%s','%s','%s','%s')" % (
            timeStamp, title, detailNew, imgs)

            try:
                cursor.execute(sql)
            except Exception as e:
                time.sleep(1)
                print(e)




if __name__ == '__main__':
    getData()