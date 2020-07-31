# coding:utf-8
from userAgents import get_html
import json
from flask import Flask
import redis
import pymysql
from flask_cors import *
import logging

fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S %a'
logging.basicConfig(level=logging.ERROR,
format=fmt,
datefmt=datefmt,
filename="/dev/null")



r = redis.Redis(host='127.0.0.1', port=6379,decode_responses=True)

app = Flask(__name__)
CORS(app)#解决跨域


@app.route('/python/symbol/<symbol>/period/<period>/size/<int:size>')
def get_hongbao(symbol,period,size):
    try:
        data = []
        data_youxu = r.zrange('market:' + symbol + ':' + period + ':redisSortset3.2.12', 0, size - 1, desc=True)
        # 由于有序集中存储的是dic，故应将每一部分转化成json再通过接口给返回
        # print(data_youxu)
        for str1 in data_youxu:
            #字典形式的字符串  转字典，eval()
            # print(str1)
            data_dict = eval(str(str1))
            #字典直接压入数组中
            data.append(data_dict)
        #将数组用json.dumps 转化即可形成标准json串
        data = json.dumps(data)
        return data
    except Exception as e:
        logging.error(e)
#从redis中读取usdt买入价格卖出价格存入redis中。
#{buy:7.1,sell:7.11}buy:平台买入，sell平台卖出
@app.route('/python/usdt_price')
def get_buy():
    try:
        a = r.get('usdt_price')
        logging.info(a)
        return a
    except Exception as e:
        logging.error(e)


#从redis中获取停盘状态，接口返回铜盘状态的json串。
@app.route('/python/state')
def get_state():
    try:
        m = {}
        A = {'44486': 'a50', '14958': 'ixic', '8984': 'hsi', '1043109': 'wti', '8862': 'trq', '8836': 'byy',
             '8831': 'mjt', '8830': 'mhj', '40717': 'dax', '1': 'eur-usd', '2': 'gbp-usd', '3': 'usd-jpy',
             '2111': 'usd-cny', '2091': 'usd-aud', '940801': 'csi300-chart','8832':'kc','58':'nzd-jpy'}
        for i in A:
            m[A.get(i)] = r.get(A.get(i))
        return json.dumps(m)
    except Exception as e:
        logging.error(e)


#从redis中读取mysql中最近3条区块链见闻新闻内容。
@app.route('/python/xinwen')
def get_xinwen():
    try:
        a = r.get('data')
        return a
    except Exception as e:
        logging.error(e)


#从redis中读取mysql中最近3条区块链见闻新闻内容。
@app.route('/python/xinwen/news')
def get_xinwen_news():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')
        cursor = conn.cursor()

        sql = "select * from hz_ada ORDER BY time1 DESC LIMIT 0,3"
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id': a[i][0], 'time': a[i][1], 'title': a[i][2], 'content': a[i][3], 'src': a[i][4]}
            L.append(dict)
        L = json.dumps(L, ensure_ascii=False, indent=4)
        # 关闭mysql链接
        cursor.close()
        conn.close()
        return L

    except Exception as e:
        logging.error(e)

#从数据库中查询具体id的那一条数据
@app.route('/python/meilin/<int:n>')
def meilin(n):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')
        cursor = conn.cursor()
        sql = "select * from hz_ada where id=" + str(n)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':a[i][0],'time': a[i][1],'title': a[i][2], 'content': a[i][3],'src' : a[i][4]}
            L.append(dict)
        L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)

#美林汇通资讯，从数据库中读出数据，每20条一页，传给我要第几页数据，返回第几页数据。
#疑问：查清楚数据源在哪？
@app.route('/python/meilin/page=<int:page>')
def meilin_page(page):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')
        cursor = conn.cursor()

        if page == 0 or page == 1:
            page = 1
        sql = "select * from hz_ada ORDER BY time1 DESC LIMIT " + str(int((20 * page)-20)) + ','+ str(20)
        cursor.execute(sql)
        a = cursor.fetchall()
        L = []
        for i in range(0, len(a)):
            dict = {'id':a[i][0],'time': a[i][1],'title': a[i][2], 'content': a[i][3],'src' : a[i][4]}
            L.append(dict)
        L = json.dumps(L, ensure_ascii=False, indent=4)
        #关闭mysql链接
        cursor.close()
        conn.close()
        return L
    except Exception as e:
        logging.error(e)

#此接口返回美元兑换人民币价格。下面火币网接口可以查到实时汇率。
@app.route('/python/mei_ren')
def mei_ren():
    try:
        html = str(7.0299)
        return html
    except Exception as e:
        logging.error(e)

#火币网各个各国家币种价格汇率，此处只展示了usdt兑换人民币的
@app.route('/python/usdt_cny')
def get_usdt_cny():
    try:
        i=r.get('usdt_cny')
        return str(i)
    except Exception as e:
        logging.error(e)

#英为才情usdt兑换日元的币种价格汇率
@app.route('/python/usdt_jpy')
def get_usdt_jpy():
    try:
        i=r.get('usdt_jpy')
        return str(i)
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 10080)

