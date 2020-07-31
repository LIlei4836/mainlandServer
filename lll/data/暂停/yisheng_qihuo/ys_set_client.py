import asyncio
import websockets
import time
import json
import os

async def hello():
    while 1:
        try:
            async with websockets.connect('ws://127.0.0.1:875')as websocket:
                data = {'key':'test'}
                await websocket.send(json.dumps(data))
                print('test')
                time.sleep(30)
                pass

        except Exception as e:
            print('调用shell脚本重启server端')
            os.system('/root/lll/data/yisheng_qihuo/restart_ys_set_server.sh')
            time.sleep(10)


asyncio.get_event_loop().run_until_complete(hello())