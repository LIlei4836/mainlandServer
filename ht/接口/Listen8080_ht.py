#!/usr/bin/python3
#coding: utf-8
from flask import Flask
import json
import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


app = Flask(__name__)
@app.route('/symbol/<symbol>/period/<period>/size/<int:size>')
def get_hongbao(symbol,period,size):
    data=r.get('market:' + symbol + ':' + period)

    try:
        data = json.loads(data)
        data = data[0:int(size)]
        data = json.dumps(data)
    except:
        return ''
    return data
if __name__ == '__main__':
    # print('http://127.0.0.1:8080/symbol/btcusdt/period/15min/size/4')
    app.run(host='0.0.0.0',port=8080)
