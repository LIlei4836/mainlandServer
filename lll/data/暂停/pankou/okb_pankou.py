from websocket import create_connection
import gzip
import time
import json
import redis
import threading
import requests
from utils import get_html,get_html_bytes

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b):
    while 1:
        try:

            t = time.time()
            timeStamp = int(round(t * 1000))
            # url = 'https://www.okex.me/v2/spot/markets/deep-deal?t=' + str(timeStamp) + '&symbol=okb_usdt'
            urlDict = ['https://www.okex.me/v2/spot/markets/deep-deal?t=', str(timeStamp), '&symbol=okb_usdt']
            url = ''.join(urlDict)
            # print(url)
            html = get_html(url)
            result = json.loads(html)
            result = result['data']
            asks = result['asks']
            bids = result['bids']

            res = {}
            res['time'] = int(time.time())
            res['sell'] = asks[0]['price']
            res['buy'] = bids[0]['price']
            res['sellmount'] = asks[0]['totalSize']
            res['buymount'] = bids[0]['totalSize']

            r.set('handicap:' + b + ':1min', json.dumps(res))
            # print(b, r.get('handicap:' + b + ':1min'))

            time.sleep(0.5)
        except:
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
