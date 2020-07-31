#!/bin/sh
kill 9 `lsof -t -i:999`
nohup python3 -u /hlg/ht/服务器999/socketHt/serHt.py> /dev/null 2>&1 &

