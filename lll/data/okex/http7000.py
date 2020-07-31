#!/usr/bin/python3
#coding: utf-8
from flask import Flask
import json
import redis
import pymysql

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

app = Flask(__name__)
@app.route('/python/symbol/<symbol>/period/<period>/size/<int:size>')
def get_hongbao(symbol, period, size):
    data = []
    result = r.get('market:' + symbol + ':' + period)
    print('market:' + symbol + ':' + period)
    # result=json.loads(result)
    # datas = eval(result['data'])
    # if size>len(datas):
    #     for i in range(len(datas)):
    #         data.append(list(reversed(datas))[i])
    # else:
    #     for i in range(size):
    #         data.append(list(reversed(datas))[i])
    #
    # data = json.dumps(data)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7000)
# get_hongbao()