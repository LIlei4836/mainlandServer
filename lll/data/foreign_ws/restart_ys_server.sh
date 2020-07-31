#!/bin/sh
kill 9 `lsof -t -i:888`
nohup python3 -u /root/lll/data/foreign_ws/ser_shengji_yisheng.py> /dev/null 2>&1 &

