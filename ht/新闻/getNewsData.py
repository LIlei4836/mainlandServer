import requests
from utils import get_html,get_html_bytes
from bs4 import BeautifulSoup
import re
import pymysql
import contextlib
import time
import logging

fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S %a'
logging.basicConfig(level=logging.INFO,
format=fmt,
datefmt=datefmt,
filename="error.log")



@contextlib.contextmanager
# def mysql(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1',charset='utf8'):
def mysql(host='127.0.0.1', port=3306, user='root', passwd='BXrXpK7Z7dSEK9lK',
          db='sj', charset='utf8'):
# def mysql(host='localhost', port=3306, user='root', passwd='root',
#           db='huihuang', charset='utf8'):
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
        sql2 = """CREATE TABLE IF NOT EXISTS qm_information(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY comment '主键',
            addtime INT comment '添加时间',
            title VARCHAR(200) comment '新闻标题',
            content VARCHAR(8000)  comment '内容')ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        cursor.execute(sql2)
        print('创建成功！')

def getAllNews():
    url = 'http://finance.sina.com.cn/blockchain/'
    html = get_html_bytes(url)

    soup = BeautifulSoup(html, 'lxml')
    newsList = soup.select('.col2-newsList li a')

    timeStampLists = []
    data = selectNews()
    for new in data:
        newTimeStamp = new['addtime']
        # print(newTimeStamp)
        timeStampLists.append(newTimeStamp)


    for tag in soup.find_all(href=re.compile("https://finance.sina.com.cn/")):
        if tag in newsList:
            href = tag.get('href')
            if 'zt_d' not in href:
                news = get_html_bytes(href)
                detailSoup = BeautifulSoup(news, 'lxml')


                detailTitle, timeStamp, detailNew = getNewDetail(detailSoup)
                # break
                with mysql() as cursor:

                    if timeStamp in timeStampLists:
                        pass
                    else:
                        sql = "insert into qm_information(title, addtime, content)values('%s','%d','%s')" % (
                            detailTitle, timeStamp, detailNew)
                        try:
                            cursor.execute(sql)
                            logging.info('添加成功')
                            timeStampLists.append(timeStamp)
                        except Exception as e:
                            time.sleep(10)
                            print(e)
                            logging.error('error')



def getNewDetail(detailSoup):

    # 获取标题
    detailTitle = detailSoup.select('.second-title')[0].get_text()

    # 发布时间转化为时间戳
    detailTime = detailSoup.select('.date')[0].get_text()
    year = detailTime[0:4]
    month = detailTime[5:7]
    day = detailTime[8:10]
    hour = detailTime[12:14]
    minute = detailTime[15:17]
    standTime = str(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00')
    timeArray = time.strptime(standTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))



    # 获取正文
    detailNews = detailSoup.select('#artibody')
    detailNew = ''
    for detailsNew in detailNews:
        for newList in detailsNew.select('p'):

            detailNew += newList.get_text()
            detailNew = str(detailNew) + str(r'\n')

    return detailTitle, timeStamp, detailNew

def selectNews():
    with mysql() as cursor:
        select_sql = "select * from qm_information"
        cursor.execute(select_sql)  # 执行SQL语句
        data = cursor.fetchall()  # 通过fetchall方法获得数据
    return data

def delNews():
    data = selectNews()
    with mysql() as cursor:
        if len(data) > 50:
            del_sql = "delete from qm_information order by addtime limit %d "%(len(data)-50)
            cursor.execute(del_sql)
            # logging.info('info')

if __name__ == '__main__':
    # chuangjian()
    getAllNews()
    # delNews()

