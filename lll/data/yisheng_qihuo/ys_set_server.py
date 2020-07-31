import websockets
import asyncio
import redis
import time
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

class WSserver():
    async def handle(self, websocket, path):
        recv_msg = await websocket.recv()
        try:
            result = json.loads(recv_msg)
            key = result['key']
            r.set(key, json.dumps(result))
            # print(key)
            print(json.dumps(result))
        except Exception as e:
            print(e)
            # time.sleep(10)
            pass

        # print(recv_msg)
        # result = r.get(recv_msg)
        # await websocket.send(result)

    def run(self):
        ser = websockets.serve(self.handle, "0.0.0.0", "875")
        asyncio.get_event_loop().run_until_complete(ser)
        asyncio.get_event_loop().run_forever()

ws = WSserver()
ws.run()
