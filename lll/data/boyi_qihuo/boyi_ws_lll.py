# -*- coding = utf-8  -*-
# @Time: 2020/5/16 11:01
# @Author: 李雷雷
# @File: boyi_ws_lll.py


import time
import json
from utils import get_html, get_html_bytes
import threading
import redis


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


def getdata(symbol,currsname,):
    while 1:
        try:
            t = str(int(time.time() * 1000))

            url = 'https://byds.anrunjf.com/quota/quota/getQuotaDataAllByWeb.do?contractsCode=' + symbol + '&_=' + t
            # 'https://byds.anrunjf.com/quota/quota/getQuotaDataAllByWeb.do?contractsCode=NG2006&_=1590044792048'

            # print(url)
            html = get_html(url)


            if 'data' in html:
                data = json.loads(html)

                result = data['data']

                if result.get('lastPrice') >0:
                    lastData = {}
                    lastData['id'] = int(str(result['upTime'])[0:10])+1
                    lastData['symbol'] = result['instrumentId'].lower()
                    lastData['open'] = result['openPrice']
                    lastData['low'] = result['lowestPrice']
                    lastData['high'] = result['highestPrice']
                    lastData['close'] = result['lastPrice']
                    lastData['vol'] = result['volume']
                    lastData['askPrice'] = result['askPrice']
                    lastData['bidPrice'] = result['bidPrice']

                    r.set('sub:' + currsname + ':' + '1min', json.dumps(lastData))
                    # print(r.get('sub:' + currsname + ':' + '1min'))
                    print('sub:' + currsname + ':' + '1min')

                    # print(t[0:10], str(result.get('upTime'))[0:10])
            time.sleep(0.05)
        except Exception as e:
            time.sleep(0.5)
            # print(e)



if __name__ == '__main__':

    #     美原油2007,美黄金2008,恒指2006,小恒指2006,德指2006,小道指2006
    #     美白银2007,天然气2007,美铜2007,A5006,小纳指2006
    #     沪深300，中证500，上证50，沪银2006，原油2007，沪镍2007，天然橡胶2009，热卷2010，螺纹钢2010，白糖009，豆粕2009，棕榈油2009,豆油2009
    A = {'CL2007':'cl2007','GC2008':'gc2008','HSI2006':'hsi2006','MHI2006':'mhi2006','DAX2006':'dax2006','YM2006':'ym2006',
         'SL2007':'sl2007','NG2007':'ng2007','HG2007':'hg2007','CN2006':'cn2006','NQ2006':'nq2006',
         'IF2006':'if2006','IC2006':'ic2006','IH2006':'ih2006','ag2006':'ag2006','sc2007':'sc2007','ni2007':'ni2007',
         'ru2009':'ru2009','hc2010':'hc2010','rb2010':'rb2010','SR009':'sr009','m2009':'m2009','p2009':'p2009','y2009':'y2009'}



    # A = {'GC2008':'gc2008'}
    threadList = list()
    for symbol in A:
        t1 = threading.Thread(target=getdata, args=(symbol, A.get(symbol), ))
        t1.start()
        threadList.append(t1)
    for t2 in threadList:
        t2.join()
