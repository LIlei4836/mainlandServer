import json
from userAgents import get_html
import time
import redis

r = redis.Redis(host = '127.0.0.1',port=6379)

def get_buy():
    while 1:
        try:
            url = "https://otc-api-hk.eiijo.cn/v1/data/trade-market?coinId=2&currency=1&tradeType=sell&currPage=1&payMethod=0&country=37&blockType=general&online=1&range=0&amount="
            res = get_html(url)
            res = json.loads(res)
            buy = res["data"][0]['price']

            time.sleep(2)

            url1 = "https://otc-api-hk.eiijo.cn/v1/data/trade-market?coinId=2&currency=1&tradeType=buy&currPage=1&payMethod=0&country=37&blockType=general&online=1&range=0&amount="
            res1 = get_html(url1)
            res1 = json.loads(res1)
            sell = res1["data"][0]['price']

            #当火币网法币交易价格出现极端行情，项目不更新价格。
            data=json.loads(r.get('usdt_price'))
            a=abs(float(buy)-float(data['buy']))
            b=abs(float(sell)-float(data['sell']))
            if a<0.05 and b<0.05:
                my_dict = {'buy': str(buy),'sell':str(sell)}
                my_dict = json.dumps(my_dict)
                print('usdt_price',my_dict)
                r.set('usdt_price',my_dict)
            time.sleep(2)
        except:
            time.sleep(2)
            pass
        try:
            #获取火币网数字货币美元价 对应人民币报价
            url = 'https://www.huobi.me/-/x/general/exchange_rate/list?r=gkb1fk'
            res = get_html(url)
            res = json.loads(res)
            for i in res['data']:
                if i['name'] == 'usdt_cny':
                    i = str(i['rate'])
                    print('usdt_cny', i)
                    r.set('usdt_cny', i)
            time.sleep(30)
        except:
            pass
        time.sleep(40)

if __name__ == '__main__':
    get_buy()