# -*- coding=utf-8  -*-
# @Time: 2020/7/18 10:37
# @Author: LeiLei Li
# @File: news_huoXingCaiJing.py


import requests,json,time
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

    sql2 = """CREATE TABLE IF NOT EXISTS news_huoXingCaiJing(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        releaseTime VARCHAR (50),
        title VARCHAR (100) ,
        content VARCHAR (2000),
        src_url VARCHAR (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=Myisam DEFAULT CHARSET=utf8;"""

    with mysql() as cursor:
        try:
            cursor.execute(sql2)
        except Exception as e:
            time.sleep(1)
            print(e)



def getNewsData():
    url = 'https://www.huoxing24.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    html = requests.get(url, headers=headers, timeout=5, )
    if html.status_code == 200:
        res = html.text
        bs = BeautifulSoup(res, 'html.parser')
        newsLists = bs.select('#newsBlock10002 > div.news-list-content > div')
        for newsList  in reversed(newsLists):
            # guanggao = newsList.select('#newsBlock10002 > div.news-list-content > div')
            # print(guanggao)
            aList = newsList.find_all('a')[0]
            href = aList.get('href')
            title = aList.get('title')
            img = newsList.find_all('img')[0].get('data-src')

            newsHtml = requests.get(href, timeout=5,)


            if newsHtml.status_code == 200:
                response = newsHtml.text
                soup = BeautifulSoup(response,'html.parser')



                dateTime = soup.select('#root > div > div.layout-content > div.layout-main.news-details > div.layout-left > div.news-details-content > div.news-info > time')

                if not dateTime:
                    continue

                time1 = dateTime[0].get_text()
                now = time.strftime("%H:%M", time.localtime())
                releaseTime = time1+' '+now

                detailLists = soup.select('#newsDetailsContent > div > p')

                # 获取正文
                detailNews = detailLists
                detailNew = ''
                for detailsNew in detailNews:
                    detailNew += detailsNew.get_text()
                    detailNew = str(detailNew) + str(r'\n')

                if not detailNew:
                    continue

                filter_list = ["APP", "阿姨", "网红"]
                if any(filterName in detailNew for filterName in filter_list):
                    continue

                with mysql() as cursor:
                    sql = "insert into news_huoXingCaiJing(time1,releaseTime, title, content,src_url)VALUES ('%s','%s','%s','%s','%s')" % (
                        time1, releaseTime, title, detailNew, img,)

                    try:
                        cursor.execute(sql)
                    except Exception as e:
                        time.sleep(1)
                        print(e)


if __name__ == '__main__':
    # chuangjian()
    getNewsData()