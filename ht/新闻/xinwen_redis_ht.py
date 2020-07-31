import requests
from lxml import etree
import pymysql
from userAgents import get_html
import time


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='BXrXpK7Z7dSEK9lK', database='sj')
cursor = conn.cursor()


def chuangjian():

    sql2 = """CREATE TABLE IF NOT EXISTS hz_ada(
        id  INT not null PRIMARY KEY auto_increment comment '主键自动增长',
        time1 VARCHAR(50) ,
        title VARCHAR (100) ,
        content VARCHAR (2000),
        src_url VARCHAR (200),
        UNIQUE KEY `time1_title` (`time1`,`title`))  ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    cursor.execute(sql2)
    print('创建成功！')
    conn.commit()

def shuju():
    while 1 :
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')
            cursor = conn.cursor()

            url1 = "http://www.qkljw.com/"
            res = get_html(url1)
            html1 = etree.HTML(res)
            li_list = html1.xpath('//*[@id="u_news_list"]/li')
            for li in li_list:
                url ='http://www.qkljw.com' + li.xpath('./a/@href')[0]
                jpg ='http://www.qkljw.com' + li.xpath('./a/div/img/@src')[0]

                response = get_html(url)
                html = etree.HTML(response)
                p_list = html.xpath('//div[@class="content"]/p')
                title = str(html.xpath('//*[@id="play_title"]/h1/text()')[0]).strip()
                time2 = str(html.xpath('//p[@class="time"]/text()')[0]).strip()
                content = []
                for p in p_list:

                    text = p.xpath('.//span/text()')
                    text1 = p.xpath('.//text()')
                    if text:
                        txt = text[0]
                        content.append(txt)
                    if text1:
                        txt1 = text1[0]
                        content.append(txt1)

                    string = ''.join(content)
                    string = string.replace('Libra\'s "virtual currency"', '')

                try:
                    if content:
                        sql2 = "insert into hz_ada(time1,title,content,src_url)VALUES ('%s','%s','%s','%s')" % (time2, title, string,jpg)
                except :
                    sql2 = "update hz_ada set time1='%s',title='%s',content='%s',src_url = '%s' where time1='%s' and title='%s'" % (time2, title, string,jpg,time2,title)
                cursor.execute(sql2)
                conn.commit()

        except:
            pass
        cursor.close()
        # 关闭光标对象
        conn.close()
        time.sleep(100)

if __name__ == '__main__':
    # chuangjian()
    shuju()


