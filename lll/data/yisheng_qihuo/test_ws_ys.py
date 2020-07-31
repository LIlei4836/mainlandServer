import time
import websockets
import asyncio
from multiprocessing import Pool
import threading
import redis

heyues = ['SGX|Z|CL|MAIN']
timeDicts = {'1min'}

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getData(heyue, time1):
    heyueList = heyue.split('|')
    heyue1 = heyueList[2].lower() + ':' + heyueList[3].lower()
    while 1:
        tradeStr = 'sub:' + heyue1 + ':' + time1
        result = r.get(tradeStr)
        print(result)
        time.sleep(0.01)


def getHeYue(time1):
    for heyue in heyues:
        t1 = threading.Thread(target=getData, args=(heyue, time1))
        t1.start()
    t1.join()

if __name__ == '__main__':
    p = Pool(len(timeDicts))
    for i in timeDicts:
        p.apply_async(getHeYue, args=(i,))
    p.close()
    p.join()