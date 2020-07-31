# -*- coding=utf-8  -*-
# @Time: 2020/7/18 10:37
# @Author: LeiLei Li
# @File: Demo04.py


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

    sql2 = """CREATE TABLE IF NOT EXISTS news_erDuoCaiJing(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        title VARCHAR (100) ,
        content VARCHAR (2000),
        src_url VARCHAR (200),
        img VARCHAR (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=Myisam DEFAULT CHARSET=utf8;"""

    with mysql() as cursor:
        try:
            cursor.execute(sql2)
        except Exception as e:
            time.sleep(1)
            print(e)



def getNewsData():
    url = 'http://www.iterduo.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    html = requests.get(url, headers=headers, timeout=5, )
    if html.status_code == 200:
        res = html.text
        bs = BeautifulSoup(res, 'lxml')
        # print(bs)
        newsLists = bs.select('body > div.container-fluid.padding0 > div > div.leftbox > div.news > ul > li')
        for news in reversed(newsLists):
            img = news.find_all('img')[0].get('src')
            Allimg = img.split('?')[0]


            title = news.select('.cl101D37')[1].get_text()

            src = news.select('.cl101D37')[1].get('href')
            newsrc = 'http://www.iterduo.com/' + src


            newhtml = requests.get(newsrc, headers=headers, timeout=5, )
            if newhtml.status_code == 200:
                newres = newhtml.text

                soup = BeautifulSoup(newres, 'lxml')
                newsTime = soup.select(
                    'body > div.container-fluid.padding0 > div > div.leftbox > div > p > span:nth-child(3)')
                releaseTime = '发布日期：'+newsTime[0].get_text()


                newsDetail = soup.select(
                    'body > div.container-fluid.padding0 > div > div.leftbox > div > div > div > p')

                # 获取正文
                detailNews = newsDetail
                detailNew = ''
                for detailsNew in detailNews:
                    detailNew += detailsNew.get_text()
                    detailNew = str(detailNew) + str(r'\n')

                # if 'APP' in detailNew or '阿姨' in detailNew or '网红' in detailNew:
                filter_list = ["APP", "阿姨", "网红"]

                if any(filterName in detailNew for filterName in filter_list):
                    continue

                with mysql() as cursor:
                    sql = "insert into news_erDuoCaiJing(time1,title,content,src_url,img)VALUES ('%s','%s','%s','%s','%s')" % (
                        releaseTime, title, detailNew, img,Allimg)

                    try:
                        cursor.execute(sql)
                    except Exception as e:
                        time.sleep(1)
                        print(e)


if __name__ == '__main__':
    chuangjian()
    getNewsData()