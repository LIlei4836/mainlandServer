#!/bin/sh
ps -ef | grep cli_shengji_yisheng.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
nohup python3 -u /root/lll/data/foreign_ws/cli_shengji_yisheng.py> /dev/null 2>&1 &

