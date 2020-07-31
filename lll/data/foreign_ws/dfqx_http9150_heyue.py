#!/usr/bin/python3
#coding: utf-8
from flask import Flask
import json
import redis
import pymysql

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

app = Flask(__name__)
@app.route('/python/getHeyueLists')
def get_heyue():
    heyues = {'CFFEX|F|IF|2006':'沪深300','INE|F|SC|2005':'原油2005','INE|F|SC|2006':'原油2006','SHFE|F|AU|2006':'沪金2006',
        'SHFE|F|AU|2010':'沪金2010','DCE|F|M|2009':'豆粕2009','DCE|F|M|2101':'豆粕2101','DCE|F|JM|2009': '焦炭2009',
        'DCE|F|JM|2101':'焦炭2101','ZCE|F|SR|009':'白糖009','ZCE|F|SR|101':'白糖101',
        'SHFE|F|RB|2010':'螺纹2010','SHFE|F|RB|2101':'螺纹2101','SHFE|F|CU|2006':'沪铜2006','SHFE|F|CU|2007':'沪铜2007',
        'SHFE|F|NI|2006':'沪镍2006','SHFE|F|NI|2007':'沪镍2007','SHFE|F|RU|2009':'沪胶2009','SHFE|F|RU|2101':'沪胶2101',
        'DCE|F|JD|2009':'鸡蛋2009','DCE|F|JD|2101':'鸡蛋2101',}

    newHeyues = {'HIHSI05': '恒指2005', 'HIHSI06': '恒指2006', 'NECLM0': '美原油2006', 'NECLN0': '美原油2007', 'HIMHI05': '小恒指2005',
         'HIMHI06': '小恒指2006', 'CMGCM0': '美黄金2006', 'CMGCN0': '美黄金2007', 'CEYMM0': '小道指2006', 'CEYMU0': '小道指2009',
         'CENQM0': '小纳指2006', 'CENQU0': '小纳指2009', 'WGCNK0': '富时A5005', 'WGCNM0': '富时A5006', }

    timeDicts = {'1min': [1,'M'],'5min':[5,'M'],'15min':[15,'M'],'30min':[30,'M'],'60min':[60,'M'],'1day':[1,'D'],'1week':[7,'D'],}

    resultLists = {}
    for heyue in heyues:
        heyueList = heyue.split('|')
        heyue1 = heyueList[2].lower() + ':' + heyueList[3].lower()

        resultDict = {}
        resultDict['socket_Key'] = 'sub:' + heyue1 + ':1min'
        # print(result)
        timeLists = list()
        for timeDict in timeDicts:
            timeData = {}
            timeData[timeDict] = f'http://39.100.233.117:8240/python/symbol/{heyueList[2].lower()}/type/{heyueList[3].lower()}/period/{timeDict}/size/300'
            timeLists.append(timeData)
            resultDict['history_key'] = timeLists
        resultLists[heyues[heyue]] = resultDict
    newtimeDicts = {'1min': [1, 'M'], '5min': [5, 'M'], '15min': [15, 'M'], '30min': [30, 'M'], '60min': [60, 'M'],
                 '1day': [1, 'D']}
    for newHeyue in newHeyues:
        resultDict = {}
        resultDict['socket_Key'] = 'sub:' + newHeyue.lower() + ':1min'
        timeLists = list()
        for timeDict in newtimeDicts:
            timeData = {}
            timeData[timeDict] = f'http://39.100.233.117:8989/symbol/{newHeyue.lower()}/period/{timeDict}/size/300'
            timeLists.append(timeData)
            resultDict['history_key'] = timeLists

        resultLists[newHeyues[newHeyue]] = resultDict
    # print(resultLists)
    return json.dumps(resultLists)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9150,debug=True)
    get_heyue()



