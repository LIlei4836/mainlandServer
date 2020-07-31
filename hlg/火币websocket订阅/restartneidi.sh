#!/bin/sh
kill 9 `lsof -t -i:998`
nohup python3 -u /hlg/hlg/火币websocket订阅/ser_shengji.py> /dev/null 2>&1 &

