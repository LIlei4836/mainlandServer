# -*- coding=utf-8  -*-
# @Time: 2020/7/18 17:55
# @Author: LeiLei Li
# @File: news_quShiChuanMei.py

import requests,json,time
from bs4 import BeautifulSoup
import contextlib
import pymysql




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

    sql2 = """CREATE TABLE IF NOT EXISTS news_quShiChuanMei(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        title VARCHAR (100) ,
        content VARCHAR (2000),
        src_url VARCHAR (200),
        img varchar (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=Myisam DEFAULT CHARSET=utf8;"""

    with mysql() as cursor:
        try:
            cursor.execute(sql2)
        except Exception as e:
            time.sleep(1)
            print(e)


def getNewsData():
    url = 'https://www.55coin.com/?s=blockchain'
    html = requests.get(url, timeout=5)
    if html.status_code == 200:
        res = html.text
        bs = BeautifulSoup(res, 'lxml')
        newsLists = bs.select('#tabNewsContent > div.tab-pane.fade.in.active > article')

        for newsList in reversed(newsLists[:-2]):

            # 固定大小图片与原图
            img = newsList.find_all('img')[0].get('src')
            AllImg = img.split('?')[0]

            # 标题
            hrefTitle = newsList.find_all('a')[0]
            href = hrefTitle.get('href')
            title = newsList.find_all('a')[2].get('title')

            # 跳转新闻详情页面
            newHtml = requests.get(href, timeout=5)
            if newHtml.status_code == 200:
                response = newHtml.text
                soup = BeautifulSoup(response, 'lxml')


                # 发布时间
                newsTime = soup.select('body > section > div > div > header > div > time')
                releaseTime = newsTime[0].get_text()

                # 获取正文
                dataLists = soup.select('body > section > div > div > article > p')
                detailNews = dataLists
                detailNew = ''
                for detailsNew in detailNews:
                    detailData = detailsNew.get_text()

                    # 过滤广告
                    if '商务合作' in detailData or '项目推广' in detailData:
                        continue

                    detailNew += detailData
                    detailNew = str(detailNew) + str(r'\n')

                with mysql() as cursor:
                    sql = "insert into news_quShiChuanMei(time1,title,content,src_url,img)VALUES ('%s','%s','%s','%s','%s')" % (
                        releaseTime, title,detailNew, img, AllImg)
                    try:
                        cursor.execute(sql)
                    except Exception as e:
                        time.sleep(1)
                        print(e)
if __name__ == '__main__':
    # chuangjian()
    getNewsData()