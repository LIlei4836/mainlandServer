# -*- coding=utf-8  -*-
# @Time: 2020/7/22 15:00
# @Author: LeiLei Li
# @File: usdt_jpy.py

import redis
import time
import json
import re
import logging
import requests


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s',
                    # filename="usdt_jpy.txt"
                    )
logging.disable(logging.CRITICAL)     # 屏蔽打印

def usdtToJpy():
    while 1:
        try:
            url = 'https://cn.investing.com/currencyconverter/service/RunConvert?fromCurrency=205&toCurrency=2&fromAmount=1&toAmount=0&currencyType=1&refreshCharts=false&dateConvert='
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
                # 'Referer':'https://cn.investing.com/currency-converter/',
                # 'Accept-Encoding':'gzip, deflate, br',
                # 'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            }

            html = requests.get(url, timeout=5, headers=headers)
            res = html.text
            data = json.loads(res)
            price = data.get('calculatedAmount')

            # usdt转日元
            if price:

                # 保留两位小数，无需四舍五入
                # priceList = re.findall(r"\d{1,}?\.\d{2}", str(price))

                # 保留两位小数，四舍五入
                # price = float('%.2f'%(float(price)))

                r.set('usdt_jpy', price)
                logging.debug(r.get('usdt_jpy'))


                # 价格波动大时，不更新
                # data = float(r.get('usdt_jpy'))
                # logging.info(data)
                # count = abs(data-price)
                # if count < 0.5:
                #     r.set('usdt_jpy', price)
                #     logging.debug(r.get('usdt_jpy'))



        except Exception as e:
            logging.info(e)
            time.sleep(30)

        time.sleep(20)


if __name__ == '__main__':
    usdtToJpy()