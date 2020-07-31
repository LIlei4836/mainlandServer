import requests
from lxml import etree
import pymysql
from userAgents import get_html
import time
from bs4 import  BeautifulSoup


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='BXrXpK7Z7dSEK9lK', database='sj')
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='123456', database='lll')
cursor = conn.cursor()





def chuangjian():

    sql2 = """CREATE TABLE IF NOT EXISTS hz_ada(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        title VARCHAR (100) ,
        content VARCHAR (2000),
        src_url VARCHAR (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=Myisam DEFAULT CHARSET=utf8;"""

    cursor.execute(sql2)
    print('创建成功！')
    conn.commit()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Connection':'keep-alive',
    'Cookie':'PHPSESSID=56dd9f7f4bb9d73815c9009ccb5dcac1; Hm_lvt_7b4f59414a31ae2cd3075ca6b130fdc0=1591426452; Hm_lpvt_7b4f59414a31ae2cd3075ca6b130fdc0=1591426513; Hm_lvt_db6865d08d553ef1668990762ee7acf8=1591426452,1591785442,1591786058,1591786450; Hm_lpvt_db6865d08d553ef1668990762ee7acf8=1591787083'
           }

def shuju():
    try:
        # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='lll')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='BXrXpK7Z7dSEK9lK', database='sj')
        cursor = conn.cursor()

        url1 = "http://www.qkljw.com/"
        html = requests.get(url1,headers=headers,timeout=10)
        res = html.text
        soup = BeautifulSoup(res, 'lxml')
        newsList = soup.select('.news ul .list')
        for new in newsList:
            img = new.select('a')[0].select('img')[0].get('src')
            # print(img)
            href = new.select('a')[0].get('href')
            url = 'http://www.qkljw.com' + href
            # print(url)
            newhtml = requests.get(url, timeout=10).text
            newsoup = BeautifulSoup(newhtml, 'lxml')

            title = newsoup.select('.tit h1')[0].text

            time1 = newsoup.select('.tit div span')[0].text
            time1 = '发布日期：'+ time1

            detailNews = newsoup.select('.main p')
            detailNew = ''
            for detailsNew in detailNews:
                detailNew += detailsNew.get_text()
                detailNew = str(detailNew) + str(r'\n')

            if '太壹科技' in title or '优盾' in detailNew:
                continue
            if '太壹科技' in detailNew or '优盾' in detailNew:
                continue

            # print(title)
            try:
                sql2 = "insert into hz_ada(time1,title,content,src_url)VALUES ('%s','%s','%s','%s')" % (time1, title, detailNew, img)
                # try:
                #     sql2 = "insert into hz_ada(time1,title,content,src_url)VALUES ('%s','%s','%s','%s')" % (time1, title, detailNew, img)
                # except Exception as e:
                #     sql2 = "update hz_ada set time1='%s',title='%s',content='%s',src_url = '%s' where time1='%s' and title='%s'" % (time1, title, detailNew, img, time1, title)
                cursor.execute(sql2)
                conn.commit()
            except Exception as e:
                print(e)
                pass


    except Exception as e:
        print(e)
        pass
    cursor.close()
    # 关闭光标对象
    conn.close()
    # time.sleep(100)


if __name__ == '__main__':
    # chuangjian()
    shuju()


