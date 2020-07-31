import requests
import time
import json
import threading
from userAgents import get_html
import redis

r = redis.Redis(host='127.0.0.1',port=6379)

def state(i,iu):
    while 1:
        try:
            t = int(time.time())
            url = "https://tvc4.forexpros.com/b85c9fa4d893c0411104d15fe4fefdca/"+str(t)+"/6/6/28/history?symbol="+i+"&resolution=1&from="+str(t-180)+"&to="+str(t)
            data = get_html(url)
            data = json.loads(data)
            if data['s'] == 'no_data':
                r.lpush('code:'+i,'1')
            else:
                r.lpush('code:'+i,'0')
            r.set(iu,r.lrange('code:' + i, 0, 0)[0].decode('utf-8'))
            if len(r.lrange('code:'+i,0,-1))>10:
                r.ltrim('code:'+i,0,0)
            time.sleep(8)
        except :
            time.sleep(10)


if __name__ == '__main__':
    A = {'44486':'a50','14958':'ixic','8984':'hsi','1043109':'wti','8862':'trq','8836':'byy','8831':'mjt','8830':'mhj','40717':'dax','1':'eur-usd','2':'gbp-usd','3':'usd-jpy','2111':'usd-cny','2091':'usd-aud','940801':'csi300-chart','8832':'kc','58':'nzd-jpy'}
    for i in A:
        t1 = threading.Thread(target=state,args=(i,A.get(i),))
        t1.start()
    t1.join()


