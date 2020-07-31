import time
import websockets
import asyncio
from multiprocessing import Pool
import threading
import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

heyues = ['COMEX|Z|GC|MAIN', 'NYMEX|Z|CL|MAIN', 'HKEX|Z|HSI|MAIN', 'HKEX|Z|MHI|MAIN', 'CME|Z|NQ|MAIN', 'COMEX|Z|HG|MAIN']
timeDicts = {'1min','5min','15min','60min','1day','30min','1week',}


async def hello(tradeStr):
    while True:
        try:
            async with websockets.connect('ws://39.99.182.181:9150')as websocket:
                await websocket.send(tradeStr)
                result = await websocket.recv()
                if result:
                    r.set(tradeStr, result)
                print(result)
                time.sleep(30)
        except Exception as e:
            time.sleep(30)



def getData(heyue, time1):
    heyueList = heyue.split('|')
    heyue1 = heyueList[2].lower() + ':' + heyueList[3].lower()
    tradeStr = 'market:' + heyue1 + ':' + time1

    asyncio.new_event_loop().run_until_complete(hello(tradeStr))


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