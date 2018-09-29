#coding=utf-8

#Author: Jiangtian
#Create Date:2018/08/04
#Last Edited:2018/08/04

#倒计时到TI8的时间。

import time

def run():
    ti8time = 1534348800
    unixtime = ti8time - time.time()
    day = (unixtime // 86400)
    hour = (unixtime % 86400) // 3600
    return [str(int(day)), str(int(hour))]
