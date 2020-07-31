# -*- coding = utf-8  -*-
# @Time: 2020/5/21 16:24
# @Author: 李雷雷
# @File: boyi_http_lll.py

from multiprocessing import  Pool
import threading
import time
import json
import requests
from utils import get_html,get_html_bytes
import redis



r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


def getname(symbol,currsname):
    B = {'1':'1min','3':'3min','5':'5min','30':'30min','60':'60min','':'1day',}
    # B = {'60':'1min',}
    threadList = list()
    for resolution in B:
        t1 = threading.Thread(target=getdata, args=(resolution,symbol,currsname,B.get(resolution)))
        t1.start()
        threadList.append(t1)
    for t2 in threadList:
        t2.join()

newDict = {'dax2006':'cedaxa0','nq2006':'cenqa0'}

def getdata(resolution,symbol,currsname,time_name):
    # print((resolution,symbol,currsname,time_name))
    while 1:
        try:
            t = str(int(time.time() * 1000))
            urlDict = ['https://byds.anrunjf.com/quota/candlestickData/getCandlesticKData.do?contractsCode=',symbol,'&type=',resolution,'&_=',t]
            url = ''.join(urlDict)
            html = get_html(url)
            if 'data' in html:
                html = json.loads(html)
                code =html.get('code')

                # 请求成功，返回200
                if code == 200:
                    data = html.get('data')
                    result = list()
                    for key,value in enumerate(data):
                        # print(data)
                        res = {}
                        res['id'] = int(str(value['timeStamp'])[0:10])+1
                        res['open'] = value['openPrice']
                        res['close'] = value['closePrice']
                        res['high'] = value['maxPrice']
                        res['low'] = value['minPrice']
                        res['vol'] = value['nowVolume']
                        res['symbol'] = currsname   # value['instrumentID'].lower() 天没有此属性
                        result.append(res)
                    if newDict.get(currsname):
                        currsname = newDict.get(currsname)
                    r.set('market:'+currsname+':'+time_name,json.dumps(result))
                    # print(json.dumps(result))
                    # print(len(data))
                    # print('market:'+currsname+':'+time_name)
                    time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)

if __name__ == '__main__':

    # A = {'CL2007':'cl2007','GC2008':'gc2008','HSI2006':'hsi2006','MHI2006':'mhi2006','DAX2006':'dax2006','YM2006':'ym2006',
    #      'SL2007':'sl2007','NG2007':'ng2007','HG2007':'hg2007','CN2006':'cn2006','NQ2006':'nq2006',
    #      'IF2006':'if2006','IC2006':'ic2006','IH2006':'ih2006','ag2006':'ag2006','sc2007':'sc2007','ni2007':'ni2007',
    #      'ru2009':'ru2009','hc2010':'hc2010','rb2010':'rb2010','SR009':'sr009','m2009':'m2009','p2009':'p2009','y2009':'y2009'}

    A = {'NQ2006':'nq2006','DAX2006':'dax2006'}


    p = Pool(len(A))
    for symbol in A:
        p.apply_async(getname, args=(symbol,A.get(symbol),))
        print('进程' + symbol + '启动成功！')
    p.close()
    p.join()