#!/bin/sh
ps -ef | grep cli_shengji.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
nohup python3 -u /hlg/hlg/火币websocket订阅/cli_shengji.py> /dev/null 2>&1 &

