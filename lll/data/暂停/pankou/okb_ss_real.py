from websocket import create_connection
import requests
import gzip
import time
import json
import redis
import threading
from utils import get_html_bytes,get_html

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b):
    while 1:
        try:
            t = time.time()
            timeStamp = int(round(t * 1000))
            # url = 'https://www.okex.me/v2/spot/markets/deals?t=' + str(timeStamp) + '&symbol=okb_usdt'
            urlDict = ['https://www.okex.me/v2/spot/markets/deals?t=', str(timeStamp), '&symbol=okb_usdt']
            url = ''.join(urlDict)
            html = get_html(url)
            result = json.loads(html)
            result = result['data']

            res = {}
            res['time'] = timeStamp
            res['amount'] = result[-1]['amount']
            res['price'] = result[-1]['price']
            if int(result[-1]['side']) == 1:
                res['type'] = 'buy'
            else:
                res['type'] = 'sell'

            r.set('real:' + b + ':1min', json.dumps(res))
            # print(r.get('real:' + b + ':1min'))

            time.sleep(0.5)
        except Exception as e:
            time.sleep(10)
if __name__ == '__main__':
    B = ['okbusdt']
    threalist = list()
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,))
        threalist.append(t1)
    for t1 in threalist:
        t1.start()
    for t1 in threalist:
        t1.join()