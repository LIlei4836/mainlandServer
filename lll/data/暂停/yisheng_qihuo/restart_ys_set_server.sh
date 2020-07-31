#!/bin/sh
kill 9 `lsof -t -i:875`
nohup python3 -u /root/lll/data/yisheng_qihuo/ys_set_server.py> /dev/null 2>&1 &

